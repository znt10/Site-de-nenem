"""Otimização de imagem no upload: redimensiona + reencoda em WebP.

Módulo puro (só Pillow + stdlib), sem Django, pra poder ter self-check rodável:
    python loja/imaging.py
"""
from io import BytesIO

from PIL import Image, ImageOps

# Knobs de calibração: qualidade/tamanho x peso do arquivo no bucket.
MAX_DIM = 1600      # maior lado da imagem, em px (só reduz, nunca amplia)
WEBP_QUALITY = 82   # 0-100; 82 é bom equilíbrio pra foto de produto


def optimize_to_webp(fileobj, max_dim=MAX_DIM, quality=WEBP_QUALITY):
    """Recebe um arquivo de imagem (aberto/uploaded) e devolve bytes WebP."""
    img = Image.open(fileobj)
    img = ImageOps.exif_transpose(img)  # respeita rotação de câmera/celular

    # WebP suporta alpha; converte pro modo certo pra reencodar.
    img = img.convert('RGBA') if 'A' in img.getbands() else img.convert('RGB')

    img.thumbnail((max_dim, max_dim))  # in-place, mantém proporção, só encolhe

    buffer = BytesIO()
    img.save(buffer, format='WEBP', quality=quality, method=6)
    return buffer.getvalue()


def _demo():
    # Gera um PNG grande e verifica que sai WebP menor e redimensionado.
    src = BytesIO()
    Image.new('RGB', (4000, 3000), (200, 120, 90)).save(src, format='PNG')
    src.seek(0)
    original_size = src.getbuffer().nbytes

    out = optimize_to_webp(src)

    assert out[:4] == b'RIFF' and out[8:12] == b'WEBP', 'saída não é WebP'
    assert len(out) < original_size, 'WebP não ficou menor que o original'
    w, h = Image.open(BytesIO(out)).size
    assert max(w, h) == MAX_DIM, f'maior lado deveria ser {MAX_DIM}, veio {max(w, h)}'
    print(f'ok: {original_size} bytes PNG -> {len(out)} bytes WebP ({w}x{h})')


if __name__ == '__main__':
    _demo()
