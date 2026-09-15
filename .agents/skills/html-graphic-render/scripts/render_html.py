from __future__ import annotations

import argparse
import base64
import hashlib
import importlib
import json
import mimetypes
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import zlib
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Self
from urllib.parse import quote, unquote, urlsplit
from urllib.request import urlopen
from xml.etree import ElementTree

from jsonschema import Draft202012Validator, FormatChecker

REMOTE_SCHEMES = {"http", "https", "ftp", "ws", "wss"}
BANNED_ELEMENTS = {
    "animate",
    "animatemotion",
    "animatetransform",
    "audio",
    "base",
    "discard",
    "embed",
    "foreignobject",
    "iframe",
    "object",
    "script",
    "set",
    "source",
    "track",
    "video",
}
NESTED_DOCUMENT_SUFFIXES = {".htm", ".html", ".xhtml"}
RESOURCE_ATTRIBUTES = {
    "cursor": ("href", "xlink:href"),
    "feimage": ("href", "xlink:href"),
    "img": ("src", "srcset"),
    "image": ("href", "xlink:href"),
    "input": ("src",),
    "link": ("href",),
    "use": ("href", "xlink:href"),
}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*(['\"])(.*?)\1\s*\)?", re.IGNORECASE)
CSS_ESCAPE = re.compile(
    r"\\(?:([0-9a-fA-F]{1,6})(?:[ \t\r\n\f])?|([^\r\n\f0-9a-fA-F]))"
)
CSS_LINE_CONTINUATION = re.compile(r"\\(?:\r\n|\r|\n|\f)")
CSS_TEMPORAL = re.compile(
    r"(?:@(?:-\w+-)?keyframes\b|\b(?:animation|transition)(?:-[a-z-]+)?\s*:)",
    re.IGNORECASE,
)
CSS_LOCAL_FONT = re.compile(r"\blocal\s*\(", re.IGNORECASE)
CSS_FONT_FACE = re.compile(r"@font-face\s*\{.*?\}", re.IGNORECASE | re.DOTALL)
CONTENT_SECURITY_POLICY = (
    "default-src 'none'; img-src 'self'; style-src 'unsafe-inline' 'self'; "
    "font-src 'self'; media-src 'none'; object-src 'none'; frame-src 'none'; "
    "script-src 'none'; connect-src 'none'; base-uri 'none'; form-action 'none'"
)
RENDER_RECORD_SCHEMA = (
    Path(__file__).resolve().parents[1] / "references/render-record.schema.json"
)


class SourceAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.css_blocks: list[str] = []
        self.copy: dict[str, str] = {}
        self.errors: list[str] = []
        self._style_depth = 0
        self._copy_key: str | None = None
        self._copy_tag: str | None = None
        self._copy_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): value or "" for name, value in attrs}
        lowered_tag = tag.lower()
        if lowered_tag in BANNED_ELEMENTS:
            self.errors.append(
                f"Active or temporal element <{lowered_tag}> is not allowed"
            )
        if (
            lowered_tag == "meta"
            and attributes.get("http-equiv", "").lower() == "refresh"
        ):
            self.errors.append("Meta refresh is not allowed")
        if any(name.startswith("on") for name in attributes):
            self.errors.append("Inline event handlers are not allowed")
        if self._copy_key is not None:
            self.errors.append(
                f"Exact-copy node {self._copy_key!r} must contain plain text only"
            )
        copy_key = attributes.get("data-copy-key")
        if copy_key:
            if copy_key in self.copy:
                self.errors.append(f"Duplicate data-copy-key {copy_key!r}")
            self._copy_key = copy_key
            self._copy_tag = lowered_tag
            self._copy_parts = []
        if lowered_tag == "style":
            self._style_depth += 1
        for attribute in RESOURCE_ATTRIBUTES.get(lowered_tag, ()):
            value = attributes.get(attribute)
            if not value:
                continue
            if attribute == "srcset":
                self.references.extend(
                    (item.strip().split()[0], "visual")
                    for item in value.split(",")
                    if item.strip()
                )
            else:
                role = (
                    "stylesheet"
                    if lowered_tag == "link"
                    and "stylesheet" in attributes.get("rel", "").lower().split()
                    else "visual"
                )
                self.references.append((value, role))
        if attributes.get("background"):
            self.references.append((attributes["background"], "visual"))
        if attributes.get("style"):
            self.css_blocks.append(attributes["style"])

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        lowered_tag = tag.lower()
        if lowered_tag == "style" and self._style_depth:
            self._style_depth -= 1
        if self._copy_key is not None and lowered_tag == self._copy_tag:
            self.copy[self._copy_key] = "".join(self._copy_parts)
            self._copy_key = None
            self._copy_tag = None
            self._copy_parts = []

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self.css_blocks.append(data)
        if self._copy_key is not None:
            self._copy_parts.append(data)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def contained(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"{label} escapes asset root: {path}")
    return resolved


def local_reference(reference: str, base: Path, root: Path) -> Path | None:
    value = reference.strip()
    if not value or value.startswith("#"):
        return None
    if value.lower().startswith("data:"):
        raise ValueError("Data URLs are not allowed; use a project-local asset")
    parsed = urlsplit(value)
    if parsed.scheme.lower() in REMOTE_SCHEMES or value.startswith("//"):
        raise ValueError(f"Remote asset is not allowed: {reference}")
    if parsed.scheme:
        raise ValueError(f"Unsupported asset scheme: {reference}")
    raw_path = unquote(parsed.path or value)
    candidate = base / raw_path
    resolved = contained(candidate, root, "Asset")
    if not resolved.is_file():
        raise ValueError(f"Local asset does not exist: {reference}")
    return resolved


def css_references(css: str) -> list[str]:
    return [reference for reference, _ in css_reference_roles(css)]


def css_reference_roles(css: str) -> list[tuple[str, str]]:
    normalized = normalize_css(css)
    import_matches = list(CSS_IMPORT.finditer(normalized))
    font_faces = list(CSS_FONT_FACE.finditer(normalized))
    references = [(match.group(2), "stylesheet") for match in import_matches]
    for match in CSS_URL.finditer(normalized):
        if any(
            imported.start() <= match.start() and match.end() <= imported.end()
            for imported in import_matches
        ):
            continue
        role = (
            "font"
            if any(
                face.start() <= match.start() and match.end() <= face.end()
                for face in font_faces
            )
            else "visual"
        )
        references.append((match.group(2), role))
    return references


def normalize_css(css: str) -> str:
    without_continuations = CSS_LINE_CONTINUATION.sub("", css)

    def replace(match: re.Match[str]) -> str:
        if hexadecimal := match.group(1):
            codepoint = int(hexadecimal, 16)
            if codepoint == 0 or codepoint > 0x10FFFF:
                return "\ufffd"
            return chr(codepoint)
        return match.group(2) or ""

    return CSS_ESCAPE.sub(replace, without_continuations)


def reject_temporal_css(css: str, label: str) -> None:
    if CSS_TEMPORAL.search(normalize_css(css)):
        raise ValueError(f"CSS animation and transition are not allowed: {label}")


def reject_temporal_or_nested_asset(path: Path, content: bytes) -> None:
    suffix = path.suffix.lower()
    if suffix in NESTED_DOCUMENT_SUFFIXES:
        raise ValueError(f"Nested HTML documents are not allowed: {path.name}")
    if suffix == ".gif" or content.startswith((b"GIF87a", b"GIF89a")):
        raise ValueError(f"Animated image formats are not allowed: {path.name}")
    if content.startswith(b"\x89PNG\r\n\x1a\n") and b"acTL" in content:
        raise ValueError(f"Animated PNG is not allowed: {path.name}")
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP" and b"ANIM" in content:
        raise ValueError(f"Animated WebP is not allowed: {path.name}")


def reject_local_font_source(css: str, label: str) -> None:
    if CSS_LOCAL_FONT.search(normalize_css(css)):
        raise ValueError(
            f"CSS local() font sources are not allowed with a required font: {label}"
        )


def svg_references(
    path: Path, text: str, reject_local_fonts: bool
) -> list[tuple[str, str]]:
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.IGNORECASE):
        raise ValueError(f"SVG declarations are not allowed: {path.name}")
    reject_temporal_css(text, path.name)
    try:
        root = ElementTree.fromstring(text)
    except ElementTree.ParseError as error:
        raise ValueError(f"Invalid SVG {path.name}: {error}") from error
    references: list[tuple[str, str]] = []
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1].lower()
        if tag in BANNED_ELEMENTS:
            raise ValueError(f"Active or temporal SVG element <{tag}> is not allowed")
        attributes = {
            name.rsplit("}", 1)[-1].lower(): value
            for name, value in element.attrib.items()
        }
        if any(name.startswith("on") for name in attributes):
            raise ValueError(f"Inline SVG event handler is not allowed: {path.name}")
        for name in ("href", "src"):
            if value := attributes.get(name):
                references.append((value, "visual"))
        if style := attributes.get("style"):
            reject_temporal_css(style, path.name)
            if reject_local_fonts:
                reject_local_font_source(style, path.name)
            references.extend(css_reference_roles(style))
        if tag == "style" and element.text:
            reject_temporal_css(element.text, path.name)
            if reject_local_fonts:
                reject_local_font_source(element.text, path.name)
            references.extend(css_reference_roles(element.text))
    return references


def audit_sources_with_snapshots(
    source: Path, root: Path, reject_local_fonts: bool = False
) -> tuple[
    dict[str, str],
    dict[str, str],
    dict[str, bytes],
    dict[str, set[str]],
]:
    root = root.resolve()
    source = source.resolve()
    parser = SourceAudit()
    source_content = source.read_bytes()
    text = source_content.decode("utf-8")
    parser.feed(text)
    parser.close()
    if parser._copy_key is not None:
        parser.errors.append(f"Unclosed exact-copy node {parser._copy_key!r}")
    for block in parser.css_blocks:
        reject_temporal_css(block, source.name)
        if reject_local_fonts:
            reject_local_font_source(block, source.name)
    if parser.errors:
        raise ValueError("; ".join(sorted(set(parser.errors))))

    pending: list[tuple[str, Path, str]] = [
        (reference, source.parent, role) for reference, role in parser.references
    ]
    pending.extend(
        (reference, source.parent, role)
        for block in parser.css_blocks
        for reference, role in css_reference_roles(block)
    )
    source_relative = source.relative_to(root).as_posix()
    files: dict[str, str] = {source_relative: content_sha256(source_content)}
    snapshots: dict[str, bytes] = {source_relative: source_content}
    roles: dict[str, set[str]] = {source_relative: {"document"}}
    processed: set[tuple[Path, str]] = set()
    while pending:
        reference, base, role = pending.pop(0)
        asset = local_reference(reference, base, root)
        if asset is None:
            continue
        relative = asset.relative_to(root).as_posix()
        roles.setdefault(relative, set()).add(role)
        if relative not in snapshots:
            content = asset.read_bytes()
            reject_temporal_or_nested_asset(asset, content)
            files[relative] = content_sha256(content)
            snapshots[relative] = content
        content = snapshots[relative]
        identity = (asset, role)
        if identity in processed:
            continue
        processed.add(identity)
        if role == "stylesheet":
            css = content.decode("utf-8")
            reject_temporal_css(css, relative)
            if reject_local_fonts:
                reject_local_font_source(css, relative)
            pending.extend(
                (value, asset.parent, nested_role)
                for value, nested_role in css_reference_roles(css)
            )
        is_svg = asset.suffix.lower() == ".svg" or content.lstrip().startswith(b"<svg")
        if role == "visual" and is_svg:
            svg = content.decode("utf-8")
            pending.extend(
                (value, asset.parent, nested_role)
                for value, nested_role in svg_references(asset, svg, reject_local_fonts)
            )
    return (
        dict(sorted(files.items())),
        parser.copy,
        dict(sorted(snapshots.items())),
        dict(sorted(roles.items())),
    )


def audit_sources(source: Path, root: Path) -> tuple[dict[str, str], dict[str, str]]:
    files, copy, _, _ = audit_sources_with_snapshots(source, root)
    return files, copy


def parse_copy(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Exact copy must use KEY=TEXT")
    key, text = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("Exact-copy key cannot be empty")
    return key, text


def browser_candidates() -> list[Path]:
    names = ["google-chrome", "chromium", "chromium-browser", "msedge"]
    discovered = [Path(value) for name in names if (value := shutil.which(name))]
    fixed = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
    ]
    for variable in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
        if value := os.environ.get(variable):
            fixed.extend(
                [
                    Path(value) / "Google/Chrome/Application/chrome.exe",
                    Path(value) / "Microsoft/Edge/Application/msedge.exe",
                ]
            )
    return discovered + fixed


def resolve_browser(explicit: Path | None) -> Path:
    if explicit is not None:
        resolved = explicit.expanduser().resolve()
        if not resolved.is_file():
            raise ValueError(f"Browser executable does not exist: {explicit}")
        return resolved
    for candidate in browser_candidates():
        if candidate.is_file():
            return candidate.resolve()
    raise ValueError("Chrome, Chromium, or Edge is required to render HTML")


def png_details(path: Path) -> tuple[int, int, bool]:
    header = path.read_bytes()[:26]
    if len(header) < 26 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Renderer did not produce a valid PNG")
    width, height = struct.unpack(">II", header[16:24])
    return width, height, header[25] in (4, 6)


def paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def png_has_transparency(path: Path) -> bool:
    content = path.read_bytes()
    position = 8
    compressed = bytearray()
    width = height = bit_depth = color_type = interlace = 0
    while position + 12 <= len(content):
        length = struct.unpack(">I", content[position : position + 4])[0]
        chunk_type = content[position + 4 : position + 8]
        data = content[position + 8 : position + 8 + length]
        position += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", data
            )
        elif chunk_type == b"IDAT":
            compressed.extend(data)
        elif chunk_type == b"IEND":
            break
    if bit_depth != 8 or color_type not in (4, 6) or interlace != 0:
        return False
    bytes_per_pixel = 2 if color_type == 4 else 4
    row_size = width * bytes_per_pixel
    decoded = zlib.decompress(bytes(compressed))
    previous = bytearray(row_size)
    offset = 0
    for _ in range(height):
        filter_type = decoded[offset]
        offset += 1
        raw = decoded[offset : offset + row_size]
        offset += row_size
        row = bytearray(row_size)
        for index, value in enumerate(raw):
            left = row[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            above = previous[index]
            upper_left = (
                previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            )
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                predictor = paeth(left, above, upper_left)
            else:
                raise ValueError(f"Unsupported PNG filter type: {filter_type}")
            row[index] = (value + predictor) & 255
        if any(
            row[index] < 255
            for index in range(bytes_per_pixel - 1, row_size, bytes_per_pixel)
        ):
            return True
        previous = row
    return False


class AssetServer:
    def __init__(
        self,
        assets: dict[str, bytes],
        content_types: dict[str, str] | None = None,
    ) -> None:
        self.assets = assets
        self.content_types = content_types or {}
        self.denied: set[str] = set()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                self._serve(include_body=True)

            def do_HEAD(self) -> None:
                self._serve(include_body=False)

            def _serve(self, include_body: bool) -> None:
                relative = unquote(urlsplit(self.path).path).lstrip("/")
                if relative == "favicon.ico":
                    self.send_error(404)
                    return
                content = owner.assets.get(relative)
                if content is None:
                    owner.denied.add(relative)
                    self.send_error(404)
                    return
                content_type = owner.content_types.get(relative)
                if content_type is None:
                    content_type = mimetypes.guess_type(relative)[0]
                self.send_response(200)
                self.send_header(
                    "Content-Type", content_type or "application/octet-stream"
                )
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                if include_body:
                    self.wfile.write(content)

            def log_message(self, format: str, *args: object) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> Self:
        self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def url(self, relative: str) -> str:
        port = self.server.server_address[1]
        return f"http://127.0.0.1:{port}/{quote(relative, safe='/')}"


class DevToolsClient:
    def __init__(self, websocket_url: str, timeout: float) -> None:
        parsed = urlsplit(websocket_url)
        if parsed.scheme != "ws" or not parsed.hostname or not parsed.port:
            raise RuntimeError("Browser returned an invalid DevTools WebSocket URL")
        self.socket = socket.create_connection((parsed.hostname, parsed.port), timeout)
        self.socket.settimeout(min(timeout, 1.0))
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {parsed.path or '/'} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.socket.sendall(request.encode("ascii"))
        response = bytearray()
        while b"\r\n\r\n" not in response:
            chunk = self.socket.recv(4096)
            if not chunk:
                raise RuntimeError("DevTools WebSocket handshake ended early")
            response.extend(chunk)
        if b" 101 " not in bytes(response).split(b"\r\n", 1)[0]:
            raise RuntimeError("DevTools WebSocket handshake failed")
        header_end = response.index(b"\r\n\r\n") + 4
        self.buffer = bytearray(response[header_end:])
        self.next_id = 1

    def close(self) -> None:
        try:
            self._send_frame(0x8, b"")
        except OSError:
            pass
        finally:
            self.socket.close()

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        length = len(payload)
        if length < 126:
            header = bytes((0x80 | opcode, 0x80 | length))
        elif length < 65536:
            header = bytes((0x80 | opcode, 0x80 | 126)) + struct.pack(">H", length)
        else:
            header = bytes((0x80 | opcode, 0x80 | 127)) + struct.pack(">Q", length)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.socket.sendall(header + mask + masked)

    def _receive_exact(self, length: int, deadline: float) -> bytes:
        content = bytearray()
        if self.buffer:
            consumed = min(length, len(self.buffer))
            content.extend(self.buffer[:consumed])
            del self.buffer[:consumed]
        while len(content) < length:
            if time.monotonic() >= deadline:
                raise RuntimeError("Timed out while reading from DevTools")
            try:
                chunk = self.socket.recv(length - len(content))
            except TimeoutError:
                continue
            if not chunk:
                raise RuntimeError("DevTools WebSocket closed unexpectedly")
            content.extend(chunk)
        return bytes(content)

    def _receive_message(self, deadline: float) -> str:
        fragments = bytearray()
        message_opcode: int | None = None
        while True:
            first, second = self._receive_exact(2, deadline)
            final = bool(first & 0x80)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._receive_exact(2, deadline))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._receive_exact(8, deadline))[0]
            mask = self._receive_exact(4, deadline) if masked else b""
            payload = self._receive_exact(length, deadline)
            if masked:
                payload = bytes(
                    value ^ mask[index % 4] for index, value in enumerate(payload)
                )
            if opcode == 0x8:
                raise RuntimeError("DevTools WebSocket closed unexpectedly")
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode in (0x1, 0x2):
                message_opcode = opcode
                fragments = bytearray(payload)
            elif opcode == 0x0 and message_opcode is not None:
                fragments.extend(payload)
            else:
                continue
            if final:
                if message_opcode != 0x1:
                    raise RuntimeError("DevTools returned a non-text message")
                return fragments.decode("utf-8")

    def call(
        self, method: str, parameters: dict[str, Any] | None, timeout: float
    ) -> dict[str, Any]:
        identifier = self.next_id
        self.next_id += 1
        message = {"id": identifier, "method": method}
        if parameters is not None:
            message["params"] = parameters
        self._send_frame(0x1, json.dumps(message, separators=(",", ":")).encode())
        deadline = time.monotonic() + timeout
        while True:
            response = json.loads(self._receive_message(deadline))
            if response.get("id") != identifier:
                continue
            if error := response.get("error"):
                raise RuntimeError(f"DevTools {method} failed: {error}")
            result = response.get("result")
            if not isinstance(result, dict):
                raise TypeError(f"DevTools {method} returned no result")
            return result


def devtools_page_url(
    profile: Path, process: subprocess.Popen[str], timeout: float
) -> str:
    active_port = profile / "DevToolsActivePort"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Browser exited before DevTools became available")
        if active_port.is_file():
            lines = active_port.read_text(encoding="utf-8").splitlines()
            if lines and lines[0].isdigit():
                endpoint = f"http://127.0.0.1:{lines[0]}/json/list"
                with urlopen(endpoint, timeout=min(timeout, 5)) as response:
                    targets = json.load(response)
                for target in targets:
                    if target.get("type") == "page" and target.get(
                        "webSocketDebuggerUrl"
                    ):
                        return str(target["webSocketDebuggerUrl"])
        time.sleep(0.05)
    raise RuntimeError("Timed out waiting for browser DevTools")


def readiness_expression(
    required_font_family: str | None,
    audited_image_urls: list[str],
    audited_font_urls: list[str],
) -> str:
    required = json.dumps(required_font_family)
    image_urls = json.dumps(audited_image_urls)
    font_urls = json.dumps(audited_font_urls)
    return rf"""
(async () => {{
  if (document.readyState !== 'complete') {{
    await new Promise(resolve => window.addEventListener('load', resolve, {{once: true}}));
  }}
  const images = await Promise.all(Array.from(document.images).map(async image => {{
    try {{ await image.decode(); }} catch (error) {{ return false; }}
    return image.complete && image.naturalWidth > 0 && image.naturalHeight > 0;
  }}));
  const auditedImages = await Promise.all({image_urls}.map(async url => {{
    const image = new Image();
    image.src = url;
    try {{ await image.decode(); }} catch (error) {{ return false; }}
    return image.complete && image.naturalWidth > 0 && image.naturalHeight > 0;
  }}));
  await document.fonts.ready;
  const requestedFamily = {required};
  const auditedFontURLs = new Set({font_urls});
  let font = null;
  if (requestedFamily) {{
    const normalize = value => value.replace(/["']/g, '').trim().toLowerCase();
    const target = normalize(requestedFamily);
    const faces = Array.from(document.fonts).filter(face => normalize(face.family) === target);
    const loaded = await Promise.all(faces.map(async face => {{
      try {{ await face.load(); return face.status === 'loaded'; }} catch (error) {{ return false; }}
    }}));
    const used = Array.from(document.querySelectorAll('[data-copy-key]')).some(element =>
      normalize(getComputedStyle(element).fontFamily.split(',')[0]) === target
    );
    const sourceURLs = [];
    const collectFontSources = rules => {{
      for (const rule of Array.from(rules || [])) {{
        if (rule.type === CSSRule.FONT_FACE_RULE &&
            normalize(rule.style.getPropertyValue('font-family')) === target) {{
          const source = rule.style.getPropertyValue('src');
          for (const match of source.matchAll(/url\(\s*(['"]?)(.*?)\1\s*\)/gi)) {{
            sourceURLs.push(new URL(match[2], document.baseURI).href);
          }}
        }} else if (rule.cssRules) {{
          collectFontSources(rule.cssRules);
        }}
      }}
    }};
    for (const sheet of Array.from(document.styleSheets)) {{
      collectFontSources(sheet.cssRules);
    }}
    font = {{
      declared: faces.length > 0,
      loaded: loaded.length > 0 && loaded.every(Boolean),
      sourcesAudited: sourceURLs.length > 0 && sourceURLs.every(url => auditedFontURLs.has(url)),
      used
    }};
  }}
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  return {{
    imagesLoaded: images.every(Boolean) && auditedImages.every(Boolean),
    animationCount: document.getAnimations({{subtree: true}}).length,
    font
  }};
}})()
"""


def run_browser(
    browser: Path,
    source: Path,
    output: Path,
    root: Path,
    snapshots: dict[str, bytes],
    asset_roles: dict[str, set[str]],
    width: int,
    height: int,
    scale: int,
    transparent: bool,
    required_font_family: str | None,
    timeout: float,
) -> str:
    source_relative = source.relative_to(root).as_posix()
    source_text = snapshots[source_relative].decode("utf-8")
    head_match = re.search(r"<head(?:\s[^>]*)?>", source_text, re.IGNORECASE)
    if head_match is None:
        raise ValueError("HTML source must contain a head element")
    policy = f'<meta http-equiv="Content-Security-Policy" content="{CONTENT_SECURITY_POLICY}">'
    hardened_text = (
        source_text[: head_match.end()] + policy + source_text[head_match.end() :]
    )
    hardened_digest = content_sha256(hardened_text.encode("utf-8"))[:16]
    hardened_relative = (
        source.parent.relative_to(root)
        / f".{source.stem}.hardened-{hardened_digest}.html"
    ).as_posix()
    served_assets = dict(snapshots)
    served_assets[hardened_relative] = hardened_text.encode("utf-8")
    content_types = {
        relative: "text/css"
        for relative, roles in asset_roles.items()
        if "stylesheet" in roles
    }
    content_types[hardened_relative] = "text/html"
    process: subprocess.Popen[str] | None = None
    client: DevToolsClient | None = None
    profile_directory = tempfile.TemporaryDirectory(prefix="html-graphic-render-")
    try:
        with AssetServer(served_assets, content_types) as assets:
            audited_image_urls = [
                assets.url(relative)
                for relative, roles in asset_roles.items()
                if "visual" in roles
            ]
            audited_font_urls = [
                assets.url(relative)
                for relative, roles in asset_roles.items()
                if "font" in roles
            ]
            profile = Path(profile_directory.name)
            process = subprocess.Popen(
                [
                    str(browser),
                    "--headless=new",
                    "--disable-background-networking",
                    "--disable-component-update",
                    "--disable-extensions",
                    "--disable-gpu",
                    "--disable-sync",
                    "--hide-scrollbars",
                    "--no-default-browser-check",
                    "--no-first-run",
                    "--run-all-compositor-stages-before-draw",
                    "--force-color-profile=srgb",
                    "--remote-debugging-port=0",
                    f"--user-data-dir={profile}",
                    "about:blank",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            client = DevToolsClient(
                devtools_page_url(profile, process, timeout), timeout
            )
            client.call("Page.enable", None, timeout)
            client.call(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": width,
                    "height": height,
                    "deviceScaleFactor": scale,
                    "mobile": False,
                },
                timeout,
            )
            if transparent:
                client.call(
                    "Emulation.setDefaultBackgroundColorOverride",
                    {"color": {"r": 0, "g": 0, "b": 0, "a": 0}},
                    timeout,
                )
            client.call(
                "Page.navigate", {"url": assets.url(hardened_relative)}, timeout
            )
            readiness = client.call(
                "Runtime.evaluate",
                {
                    "expression": readiness_expression(
                        required_font_family,
                        audited_image_urls,
                        audited_font_urls,
                    ),
                    "awaitPromise": True,
                    "returnByValue": True,
                },
                timeout,
            )
            if readiness.get("exceptionDetails"):
                raise RuntimeError("Browser readiness evaluation failed")
            state = readiness.get("result", {}).get("value")
            if not isinstance(state, dict) or not state.get("imagesLoaded"):
                raise ValueError("One or more local images failed to decode")
            if state.get("animationCount") != 0:
                raise ValueError("Browser detected an active animation")
            if required_font_family:
                font = state.get("font")
                if not isinstance(font, dict) or not all(
                    font.get(field)
                    for field in ("declared", "loaded", "sourcesAudited", "used")
                ):
                    raise ValueError(
                        f"Required local font failed to load or is unused: {required_font_family}"
                    )
            if assets.denied:
                raise ValueError(
                    "Browser requested unaudited assets: "
                    + ", ".join(sorted(assets.denied))
                )
            capture = client.call(
                "Page.captureScreenshot",
                {"format": "png", "fromSurface": True},
                timeout,
            )
            data = capture.get("data")
            if not isinstance(data, str):
                raise TypeError("Browser returned no screenshot data")
            output.write_bytes(base64.b64decode(data, validate=True))
            version = client.call("Browser.getVersion", None, timeout)
            return str(version.get("product") or browser.name)
    finally:
        if client is not None:
            client.close()
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
        profile_directory.cleanup()


def validate_dimensions(width: int, height: int, scale: int) -> None:
    if not 1 <= width <= 8192 or not 1 <= height <= 8192:
        raise ValueError("Width and height must be between 1 and 8192")
    if not 1 <= scale <= 4:
        raise ValueError("Device scale factor must be between 1 and 4")
    if width * height * scale * scale > 50_000_000:
        raise ValueError("Requested raster exceeds the 50-megapixel safety limit")


def path_key(path: Path) -> str:
    return unicodedata.normalize("NFC", str(path.resolve())).casefold()


def acquire_file_lock(handle: Any) -> None:
    if os.name == "nt":
        lock_module = importlib.import_module("msvcrt")
        if os.fstat(handle.fileno()).st_size == 0:
            handle.write("\0")
            handle.flush()
        handle.seek(0)
        lock_module.locking(handle.fileno(), lock_module.LK_LOCK, 1)
        return
    lock_module = importlib.import_module("fcntl")
    lock_module.flock(handle, lock_module.LOCK_EX)


@contextmanager
def render_target_lock(root: Path, output: Path, record: Path) -> Iterator[None]:
    target_keys = sorted({path_key(output), path_key(record)})
    handles = []
    try:
        for target_key in target_keys:
            identity = json.dumps(
                [path_key(root), target_key], separators=(",", ":")
            ).encode("utf-8")
            lock = Path(tempfile.gettempdir()) / (
                f"ark-director-html-render-{hashlib.sha256(identity).hexdigest()}.lock"
            )
            if lock.is_symlink():
                raise ValueError("Render target lock must not be a symlink")
            flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(lock, flags, 0o600)
            handle = os.fdopen(descriptor, "a")
            try:
                acquire_file_lock(handle)
            except BaseException:
                handle.close()
                raise
            handles.append(handle)
        yield
    finally:
        for handle in reversed(handles):
            handle.close()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        if temporary is None:
            raise RuntimeError("Render record staging did not create a file")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def stage_bytes(path: Path, content: bytes, suffix: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=suffix,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if temporary is None:
            raise RuntimeError("Render artifact staging did not create a file")
        return temporary
    except BaseException:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise


def stage_json(path: Path, value: dict[str, Any]) -> Path:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return stage_bytes(path, content, ".json.tmp")


def replace_file(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def transaction_path(record: Path) -> Path:
    return record.with_name(f".{record.name}.transaction.json")


def file_hash(path: Path) -> str | None:
    return sha256(path) if path.is_file() else None


def transaction_artifact(
    root: Path,
    final: Path,
    staged: Path,
) -> dict[str, str | None]:
    backup: Path | None = None
    try:
        old_hash = file_hash(final)
        backup = stage_bytes(final, final.read_bytes(), ".backup") if old_hash else None
        return {
            "path": final.relative_to(root).as_posix(),
            "staged_path": staged.relative_to(root).as_posix(),
            "new_sha256": sha256(staged),
            "old_sha256": old_hash,
            "backup_path": backup.relative_to(root).as_posix() if backup else None,
        }
    except BaseException:
        if backup is not None:
            backup.unlink(missing_ok=True)
        raise


def transaction_files(
    root: Path,
    artifact: dict[str, Any],
) -> tuple[Path, Path, Path | None]:
    final = contained(root / str(artifact["path"]), root, "Transaction output")
    staged = contained(
        root / str(artifact["staged_path"]), root, "Transaction staged file"
    )
    backup_value = artifact.get("backup_path")
    backup = (
        contained(root / str(backup_value), root, "Transaction backup")
        if backup_value
        else None
    )
    return final, staged, backup


def validate_transaction(
    value: Any,
    root: Path,
    output: Path,
    record: Path,
) -> list[dict[str, Any]]:
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Render transaction journal is invalid")
    if value.get("state") not in {"prepared", "committed"}:
        raise ValueError("Render transaction journal has an invalid state")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 2:
        raise ValueError("Render transaction journal must contain two artifacts")
    expected_paths = {output.resolve(), record.resolve()}
    resolved_paths: set[Path] = set()
    all_path_keys: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {
            "backup_path",
            "new_sha256",
            "old_sha256",
            "path",
            "staged_path",
        }:
            raise ValueError("Render transaction artifact is invalid")
        for key in ("new_sha256", "old_sha256"):
            digest = artifact.get(key)
            if digest is not None and not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
                raise ValueError("Render transaction hash is invalid")
        final, staged, backup = transaction_files(root, artifact)
        resolved_paths.add(final)
        auxiliary_paths = [staged] + ([backup] if backup is not None else [])
        if any(
            path.parent != final.parent or not path.name.startswith(f".{final.name}.")
            for path in auxiliary_paths
        ):
            raise ValueError("Render transaction auxiliary path is invalid")
        for path in [final, *auxiliary_paths]:
            key = path_key(path)
            if key in all_path_keys:
                raise ValueError("Render transaction paths must be distinct")
            all_path_keys.add(key)
    if resolved_paths != expected_paths:
        raise ValueError("Render transaction targets do not match this render")
    return artifacts


def cleanup_transaction(
    root: Path,
    journal: Path,
    artifacts: list[dict[str, Any]],
) -> None:
    for artifact in artifacts:
        _, staged, backup = transaction_files(root, artifact)
        if staged.exists():
            if file_hash(staged) != artifact["new_sha256"]:
                raise ValueError(f"Render transaction staged file changed: {staged}")
            staged.unlink()
        if backup is not None and backup.exists():
            if file_hash(backup) != artifact["old_sha256"]:
                raise ValueError(f"Render transaction backup changed: {backup}")
            backup.unlink()
    journal.unlink(missing_ok=True)


def recover_transaction(root: Path, output: Path, record: Path) -> None:
    journal = transaction_path(record)
    if not journal.exists():
        return
    value = json.loads(journal.read_text(encoding="utf-8"))
    artifacts = validate_transaction(value, root, output, record)
    if value["state"] == "committed":
        for artifact in artifacts:
            final, _, _ = transaction_files(root, artifact)
            if file_hash(final) != artifact["new_sha256"]:
                raise ValueError(f"Committed render transaction does not match {final}")
        cleanup_transaction(root, journal, artifacts)
        return
    for artifact in artifacts:
        final, _, backup = transaction_files(root, artifact)
        current_hash = file_hash(final)
        old_hash = artifact["old_sha256"]
        new_hash = artifact["new_sha256"]
        if old_hash is None:
            if current_hash == new_hash:
                final.unlink()
            elif current_hash is not None:
                raise ValueError(f"Cannot recover changed render artifact: {final}")
            continue
        if current_hash == old_hash:
            continue
        if current_hash not in {None, new_hash}:
            raise ValueError(f"Cannot recover changed render artifact: {final}")
        if backup is None or file_hash(backup) != old_hash:
            raise ValueError(f"Render transaction backup is unavailable: {final}")
        replace_file(backup, final)
    cleanup_transaction(root, journal, artifacts)


def promote_render_pair(
    root: Path,
    output: Path,
    record: Path,
    staged_output: Path,
    result: dict[str, Any],
    expected_targets: dict[Path, str | None],
) -> None:
    staged_record = stage_json(record, result)
    artifacts: list[dict[str, Any]] = []
    journal = transaction_path(record)
    journal_written = False
    try:
        artifacts.append(transaction_artifact(root, output, staged_output))
        artifacts.append(transaction_artifact(root, record, staged_record))
        for artifact in artifacts:
            final, _, _ = transaction_files(root, artifact)
            if artifact["old_sha256"] != expected_targets[final]:
                raise ValueError(f"Render target changed during rendering: {final}")
        value = {
            "schema_version": 1,
            "state": "prepared",
            "artifacts": artifacts,
        }
        atomic_json(journal, value)
        journal_written = True
        for artifact in artifacts:
            final, staged, _ = transaction_files(root, artifact)
            if file_hash(final) != artifact["old_sha256"]:
                raise ValueError(f"Render target changed during promotion: {final}")
            replace_file(staged, final)
        for artifact in artifacts:
            final, _, _ = transaction_files(root, artifact)
            if file_hash(final) != artifact["new_sha256"]:
                raise ValueError(f"Promoted render artifact hash mismatch: {final}")
        value["state"] = "committed"
        atomic_json(journal, value)
        cleanup_transaction(root, journal, artifacts)
    except BaseException:
        if journal_written:
            recover_transaction(root, output, record)
        else:
            staged_record.unlink(missing_ok=True)
            for artifact in artifacts:
                _, staged, backup = transaction_files(root, artifact)
                staged.unlink(missing_ok=True)
                if backup is not None:
                    backup.unlink(missing_ok=True)
        raise


def verify_current_inputs(root: Path, files: dict[str, str]) -> None:
    for relative, expected_hash in files.items():
        current = contained(root / relative, root, "Audited input")
        if not current.is_file() or sha256(current) != expected_hash:
            raise ValueError(f"Input changed after audit: {relative}")


def verify_current_targets(targets: dict[Path, str | None]) -> None:
    for target, expected_hash in targets.items():
        if file_hash(target) != expected_hash:
            raise ValueError(f"Render target changed during rendering: {target}")


def validate_render_record(record: dict[str, Any]) -> None:
    schema = json.loads(RENDER_RECORD_SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"Render record failed schema validation: {details}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render project-local static HTML to a fixed-size PNG"
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--asset-root", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--browser", type=Path)
    parser.add_argument("--copy", action="append", default=[], type=parse_copy)
    parser.add_argument("--transparent", action="store_true")
    parser.add_argument("--require-local-font", metavar="FAMILY")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser


def execute(arguments: argparse.Namespace) -> dict[str, Any]:
    validate_dimensions(arguments.width, arguments.height, arguments.scale)
    if not 0 < arguments.timeout <= 300:
        raise ValueError("Timeout must be greater than 0 and at most 300 seconds")
    source = arguments.source.expanduser().resolve()
    if source.suffix.lower() not in {".html", ".htm"} or not source.is_file():
        raise ValueError("Source must be an existing HTML file")
    root = (arguments.asset_root or source.parent).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("Asset root must be an existing directory")
    source = contained(source, root, "Source")
    output = contained(arguments.output.expanduser(), root, "Output")
    record_input = arguments.record or output.with_name(f"render_{output.stem}.json")
    record = contained(record_input.expanduser(), root, "Render record")
    if output.suffix.lower() != ".png":
        raise ValueError("Output must use the .png extension")
    with render_target_lock(root, output, record):
        return execute_locked(arguments, source, root, output, record)


def execute_locked(
    arguments: argparse.Namespace,
    source: Path,
    root: Path,
    output: Path,
    record: Path,
) -> dict[str, Any]:
    recover_transaction(root, output, record)
    if output.exists() and not arguments.overwrite:
        raise ValueError(f"Output already exists; choose a new version: {output}")
    if record.exists() and not arguments.overwrite:
        raise ValueError(
            f"Render record already exists; choose a new version: {record}"
        )
    prior_target_hashes = {output: file_hash(output), record: file_hash(record)}
    files, discovered_copy, snapshots, asset_roles = audit_sources_with_snapshots(
        source,
        root,
        reject_local_fonts=bool(arguments.require_local_font),
    )
    source_relative = source.relative_to(root).as_posix()
    protected_inputs = {root / path for path in files}
    output_key = path_key(output)
    record_key = path_key(record)
    if output_key == record_key or (
        output.exists() and record.exists() and os.path.samefile(output, record)
    ):
        raise ValueError("Output and render record must use different paths")
    for protected in protected_inputs:
        protected_key = path_key(protected)
        if output_key == protected_key or (
            output.exists() and os.path.samefile(output, protected)
        ):
            raise ValueError(f"Output aliases source or input asset: {protected}")
        if record_key == protected_key or (
            record.exists() and os.path.samefile(record, protected)
        ):
            raise ValueError(
                f"Render record aliases source or input asset: {protected}"
            )
    if arguments.require_local_font and not any(
        "font" in roles for roles in asset_roles.values()
    ):
        raise ValueError("A project-local font is required but none was discovered")
    required_copy = dict(arguments.copy)
    if len(required_copy) != len(arguments.copy):
        raise ValueError("Exact-copy keys must be unique")
    undeclared_copy = sorted(set(discovered_copy) - set(required_copy))
    if undeclared_copy:
        raise ValueError(
            "Every data-copy-key must have a matching --copy value: "
            + ", ".join(undeclared_copy)
        )
    for key, expected in required_copy.items():
        actual = discovered_copy.get(key)
        if actual != expected:
            raise ValueError(
                f"Exact copy mismatch for {key!r}: expected {expected!r}, got {actual!r}"
            )
    browser = resolve_browser(arguments.browser)
    script_hash = sha256(Path(__file__).resolve())
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".png",
        delete=False,
    ) as handle:
        temporary_output = Path(handle.name)
    temporary_output.unlink()
    try:
        browser_version = run_browser(
            browser,
            source,
            temporary_output,
            root,
            snapshots,
            asset_roles,
            arguments.width,
            arguments.height,
            arguments.scale,
            arguments.transparent,
            arguments.require_local_font,
            arguments.timeout,
        )
        actual_width, actual_height, has_alpha = png_details(temporary_output)
        expected_width = arguments.width * arguments.scale
        expected_height = arguments.height * arguments.scale
        if (actual_width, actual_height) != (expected_width, expected_height):
            raise ValueError(
                "PNG dimensions differ from the requested viewport: "
                f"{actual_width}x{actual_height} != {expected_width}x{expected_height}"
            )
        if arguments.transparent and not has_alpha:
            raise ValueError("Transparent output does not contain an alpha channel")
        has_transparency = (
            png_has_transparency(temporary_output) if has_alpha else False
        )
        if arguments.transparent and not has_transparency:
            raise ValueError("Transparent output contains no transparent pixels")
        fingerprint_payload = {
            "assets": files,
            "background": "transparent" if arguments.transparent else "opaque",
            "browser": browser_version,
            "copy": required_copy,
            "height": arguments.height,
            "renderer_script_sha256": script_hash,
            "required_font_family": arguments.require_local_font,
            "scale": arguments.scale,
            "width": arguments.width,
        }
        fingerprint = hashlib.sha256(
            json.dumps(
                fingerprint_payload, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        output_hash = sha256(temporary_output)
        result = {
            "schema_version": 1,
            "generation": "deterministic_html",
            "source": {
                "path": source_relative,
                "sha256": files[source_relative],
            },
            "inputs": [
                {"path": path, "sha256": digest}
                for path, digest in files.items()
                if path != source_relative
            ],
            "copy": [
                {"key": key, "text": text, "verified": True}
                for key, text in required_copy.items()
            ],
            "renderer": {
                "name": "html-graphic-render",
                "browser": browser_version,
                "script_sha256": script_hash,
                "viewport": {
                    "width": arguments.width,
                    "height": arguments.height,
                    "device_scale_factor": arguments.scale,
                },
                "background": ("transparent" if arguments.transparent else "opaque"),
                "font_policy": (
                    "project_local_required"
                    if arguments.require_local_font
                    else "platform_fallback_allowed"
                ),
                "required_font_family": arguments.require_local_font,
            },
            "input_fingerprint_sha256": fingerprint,
            "output": {
                "path": str(output.relative_to(root)),
                "mime_type": "image/png",
                "width": actual_width,
                "height": actual_height,
                "has_alpha_channel": has_alpha,
                "has_transparency": has_transparency,
                "bytes": temporary_output.stat().st_size,
                "sha256": output_hash,
            },
            "rendered_at": datetime.now(UTC).isoformat(),
        }
        validate_render_record(result)
        verify_current_inputs(root, files)
        verify_current_targets(prior_target_hashes)
        promote_render_pair(
            root,
            output,
            record,
            temporary_output,
            result,
            prior_target_hashes,
        )
        return {
            "output": str(output),
            "record": str(record),
            "mime_type": "image/png",
            "width": actual_width,
            "height": actual_height,
            "has_alpha_channel": has_alpha,
            "has_transparency": has_transparency,
            "bytes": output.stat().st_size,
            "sha256": output_hash,
        }
    finally:
        temporary_output.unlink(missing_ok=True)


def main() -> int:
    try:
        result = execute(build_parser().parse_args())
    except (
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
