# Costa Flooring LLC — site

Site estático (HTML + CSS + JS puro). O que vai pro servidor é **só a pasta `site/`**.

## Estrutura
```
site/                  ← deploy isto (raiz do domínio)
  index.html
  services/…           ← hub + 6 páginas de serviço
  service-areas/  about/  estimate/  thanks/  privacy-policy/  terms/
  404.html  sitemap.xml  robots.txt  favicon.svg
  assets/css/style.css  assets/js/main.js  assets/img/*.webp
tools/
  build.py             ← gera site/ a partir de tools/pages/*.html
  shell.py             ← header, footer, contact-bar e sidebar compartilhados (edite aqui)
  pages/*.html         ← conteúdo de cada página + meta JSON no topo
  shots.mjs / peek.mjs ← QA visual com Playwright (screenshots 390/768/1440 + overflow + console)

## Design system (v2)
- Fontes: Poppins (títulos; 2ª linha em `<em>` = itálico light cor oak) + Inter (corpo)
- Cores: walnut #3B2314 / #2A1810 · oak #C4853D · verde CTA #22A04A (gloss) · sand #F6F2EC
- Seções: 60px cima/baixo (`--section`), headline + parágrafo centralizados (`.section-head`), botão no fim (`.section__cta`); splits foto+texto ficam à esquerda
- Textura de madeira: `.section--grain` (SVG feTurbulence, opacidade baixa)
- Componentes: `.svc-card`, `.why-item`, `.timeline` (+ `.timeline--5`), `.ba` (+ `.ba-solo`), `.wall` + lightbox, `.faq__item`, `.opt` cards (`.opt-grid--2/--4`), `.check-list`
- Páginas de serviço (v2.3) seguem a home: `.hero--page` (foto + kicker + h1 com `<em>`) → split "what's included" → cards `.opt` → timeline walnut → prova (before/after, stain lab, split) → reviews → FAQ → serviços relacionados. Botão em toda dobra.
- Placeholders nas páginas: `{{ICON:nome}}` (ver `ICONS` em shell.py), `{{RELATED:refinishing,sanding,...}}` (cards de serviço), `{{REVIEWS:whitmore,collier,...}}` (reviews reais), `{{WALL:img,img|img,img}}` (portfólio de 2 fileiras; alt em `ALT` no shell.py)

## Fotos do cliente
Originais em `materiasi para o site/` (não vai pro deploy). Fluxo para escolher novas:
1. `python tools/contact.py` → folhas de contato numeradas em `tools/contact/`
2. Ajuste a lista `PICK` em `tools/pick.py` e rode → gera `site/assets/img/job-NNN-{480,960}.webp`
3. Adicione o alt em `ALT` (shell.py) e use no `{{WALL:...}}`
Regra: nada de balde, ferramenta, fita azul, entulho, pé ou obra crua na foto.
BRIEF.md               ← discovery, dados do cliente, pendências
```

## Deploy (Hostinger)
`python tools/deploy.py` gera `deploy/` (só os arquivos usados, 5 MB) e `deploy-costaflooring.zip`. Sobe o conteúdo de `deploy/` na raiz do `public_html` (ou extrai o zip lá). Inclui `.htaccess` com 404, HTTPS/non-www, trailing slash e cache.

## Editar e regerar
1. Edite `tools/pages/<pagina>.html` (ou header/footer em `tools/build.py`).
2. `python tools/build.py`
3. Teste local: `python -m http.server 8765 --directory site` → http://localhost:8765

## QA visual
`node tools/shots.mjs tools/shots` (precisa de `npm install playwright` uma vez).
Páginas específicas: `node tools/shot1.mjs <pasta-saida> /services/ /services/floor-repair/ …` (390 + 1440, força reveal e imagens lazy).

## Antes de publicar (pendências)
- [ ] Trocar `GTM-XXXXXXX` em `tools/build.py` pelo container real e regerar.
- [x] Formulários (home e /estimate/, ambos `id="form01"`) enviam via Web3Forms (`access_key` no HTML) e redirecionam para `/thanks/`. Honeypot: campo `botcheck`.
- [ ] Configurar 404 no servidor (`404.html` na raiz; no Apache: `ErrorDocument 404 /404.html`).
- [ ] Crédito "Site by Eu sou TS" no rodapé está sem link — adicionar URL se quiser.
