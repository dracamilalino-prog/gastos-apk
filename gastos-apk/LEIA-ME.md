# Gastos — APK

App de gastos empacotado com Capacitor. O APK é compilado pelo GitHub, não pelo seu computador.

---

## Passo 1 — Criar o repositório

1. Entre no GitHub com a conta `dracamilalino-prog`
2. **New repository** → nome: `gastos-apk`
3. Deixe **Public** (release pública = download direto no celular, sem login)
4. **Não** marque nenhuma opção de "Add README" — o repositório precisa nascer vazio
5. **Create repository**

## Passo 2 — Subir os arquivos

Na tela do repositório recém-criado, clique em **uploading an existing file**.

Descompacte o ZIP no computador e arraste **todo o conteúdo** da pasta (não a pasta em si) para a área de upload. Precisa subir tudo, inclusive a pasta oculta `.github` — se ela não aparecer no seu explorador de arquivos, ative "mostrar itens ocultos".

Clique em **Commit changes**.

> Se o upload pelo navegador engasgar com a quantidade de arquivos, use o GitHub Desktop ou o git pela linha de comando.

## Passo 3 — Esperar o APK

Assim que o commit entra, o build começa sozinho.

1. Aba **Actions** → verá "Gerar APK" rodando
2. Leva de **5 a 10 minutos** na primeira vez
3. Quando o ✅ verde aparecer, vá na aba **Releases** (coluna direita da página inicial do repositório)
4. Lá estará **gastos.apk**

Cada vez que você mudar o `www/index.html` e salvar, um APK novo é gerado automaticamente.

## Passo 4 — Instalar no Galaxy

1. Abra a página de Releases **pelo celular** e toque em `gastos.apk`
2. O Chrome vai avisar que o tipo de arquivo pode ser prejudicial → **Baixar mesmo assim**
3. Abra o arquivo baixado (notificação ou app **Meus Arquivos** → Downloads)
4. Vai aparecer "Por segurança, o telefone não pode instalar apps desconhecidos desta fonte" → **Configurações** → ative **Permitir desta fonte** → volte
5. **Instalar** → o Play Protect avisa que não reconhece o app → **Instalar mesmo assim**

Pronto. Ícone "Gastos" na gaveta de apps.

## Passo 5 — Levar os dados que já existem

Os dados do atalho antigo do Chrome **não passam sozinhos** para o app — são armazenamentos separados.

1. Abra o atalho antigo no Chrome
2. Toque em **↑ Exportar backup** → salva um `.json` em Downloads
3. Abra o app novo → **↓ Importar backup** → escolha esse arquivo
4. Confira o total dos meses e só então apague o atalho antigo

---

## Alterando o app depois

Todo o app está em **`www/index.html`** — um arquivo só, como antes.

- Pelo site do GitHub: abra o arquivo → ✏️ → edite → **Commit changes** → APK novo em ~7 min
- Ou me mande o arquivo alterado que eu devolvo pronto

Não mexa na pasta `android/` — ela é gerada pelo Capacitor.

## Para atualizar o app no celular

Baixe o APK novo e instale por cima. **Os dados são preservados** — o Android reconhece como atualização do mesmo app, desde que a assinatura seja a mesma (é, sempre a mesma keystore de debug do GitHub).

Só desinstale o app se quiser realmente zerar tudo — e exporte o backup antes.

---

## Detalhes técnicos

| | |
|---|---|
| ID do app | `br.com.dracamilalino.gastos` |
| Nome | Gastos |
| Android mínimo | 7.0 (API 24) |
| Assinatura | keystore de debug (não serve para publicar na Play Store) |
| Dados | `localStorage` interno do app, só neste aparelho |
| Internet | não usa, em momento nenhum |
| Plugins | `@capacitor/filesystem` e `@capacitor/share`, só para o backup |

O app não pede nenhuma permissão sensível. O `AndroidManifest` declara acesso à internet porque o Capacitor exige para o WebView local funcionar, mas nada é enviado para fora.

### Se o build falhar

Vá em **Actions** → clique no build vermelho → abra o passo que falhou. Copie a mensagem de erro e me mande que eu corrijo.
