# Costa Flooring LLC — site

Site estático (HTML + CSS + JS puro). O que vai pro servidor é **só a pasta `public/`**.

## Estrutura
```
public/                ← deploy isto (raiz do domínio)
  index.html
  services/…           ← hub + 6 páginas de serviço
  service-areas/  about/  estimate/  thanks/  privacy-policy/  terms/
  404.html  sitemap.xml  robots.txt  favicon.svg
  assets/css/style.css  assets/js/main.js  assets/img/*.webp
tools/
  build.py             ← gera public/ a partir de tools/pages/*.html
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

## Blog (`/blog/`)
- Posts em `tools/blog/NN-slug.html`: JSON no topo (slug, data, categoria `care`/`install`, title ≤60, description ~155, h1 com `<em>`, excerpt, "quick answer", foto, serviços/reviews/posts relacionados, FAQ) + corpo com `<h2 id="...">`. O sumário, tempo de leitura, schema (BlogPosting + Breadcrumb + FAQPage), OG 1200×630 (`assets/img/og-<slug>.jpg`), feed `blog/feed.xml` e o sitemap saem sozinhos.
- Template e cards: `tools/blog.py`. Diagramas: `tools/diagrams.py`.
- Placeholders no corpo: `{{CTA:refinish|repair|install|carpet|compare|dust|holiday}}`, `{{FIG:img|alt|legenda}}`, `{{FIG2:img|alt|img|alt|legenda}}`, `{{BA:hall|stairs}}`, `{{DIAGRAM:nome}}`. Em qualquer página: `{{POSTS:slug,slug,slug}}` (home e páginas de serviço já usam).
- Post novo: copie um arquivo de `tools/blog/`, troque o JSON e o texto, rode o build. Link interno: todo post linka para o serviço que explica e para 1–2 posts do mesmo cluster; ao publicar, adicione o post no `{{POSTS:...}}` da página de serviço certa.
- URLs antigas do WordPress (`/uncategorized/...`) já têm 301 em `public/.htaccess`.
- Fotos: `job-004` = `svc-sanding`, `gal-12` = `job-122`, `job-049` = `ba-install-after` são o mesmo arquivo; não use o par no mesmo post.

## Fotos do cliente
Originais em `materiasi para o site/` (não vai pro deploy). Fluxo para escolher novas:
1. `python tools/contact.py` → folhas de contato numeradas em `tools/contact/`
2. Ajuste a lista `PICK` em `tools/pick.py` e rode → gera `public/assets/img/job-NNN-{480,960}.webp`
3. Adicione o alt em `ALT` (shell.py) e use no `{{WALL:...}}`
Regra: nada de balde, ferramenta, fita azul, entulho, pé ou obra crua na foto.
BRIEF.md               ← discovery, dados do cliente, pendências
```

## Deploy (Hostinger)
`python tools/deploy.py` gera `deploy/` (só os arquivos usados, 5 MB) e `deploy-costaflooring.zip`. Sobe o conteúdo de `deploy/` na raiz do `public_html` (ou extrai o zip lá). Inclui `.htaccess` com 404, HTTPS/non-www, trailing slash e cache.

## Editar e regerar
1. Edite `tools/pages/<pagina>.html` (ou header/footer em `tools/build.py`).
2. `python tools/build.py`
3. Teste local: `python -m http.server 8765 --directory public` → http://localhost:8765

## QA visual
`node tools/shots.mjs tools/shots` (precisa de `npm install playwright` uma vez).
Páginas específicas: `node tools/shot1.mjs <pasta-saida> /services/ /services/floor-repair/ …` (390 + 1440, força reveal e imagens lazy).
Componentes: `node tools/elshot.mjs <pasta> <largura> /blog/<slug>/ ".diagram, .post-cta"` (print de cada elemento). Imagens: `node tools/imgcheck.mjs /blog/ …` (lista imagem que não carregou; o `<img src="">` do lightbox aparece sempre, é esperado).
Obs.: screenshot de página inteira acima de ~16.000px repete blocos (limite do Chrome), não é bug da página.

## Antes de publicar (pendências)
- [ ] Trocar `GTM-XXXXXXX` em `tools/build.py` pelo container real e regerar.
- [x] Formulários (home e /estimate/, ambos `id="form01"`) enviam via Web3Forms (`access_key` no HTML) e redirecionam para `/thanks/`. Honeypot: campo `botcheck`.
- [ ] Configurar 404 no servidor (`404.html` na raiz; no Apache: `ErrorDocument 404 /404.html`).
- [ ] Crédito "Site by Eu sou TS" no rodapé está sem link — adicionar URL se quiser.
