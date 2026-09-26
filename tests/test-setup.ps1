# ============================================================
#  test-setup.ps1 — Verifica o setup do projeto dedicado
#  Projeto alvo: ai-job-search-borbaf
#  Conta billing: 012110-9E0053-27291A
# ============================================================

$PROJ   = "ai-job-search-borbaf"
$BILL   = "012110-9E0053-27291A"
$PASS   = 0
$FAIL   = 0

function Check($name, $ok, $detail) {
    if ($ok) { $script:PASS++; Write-Host "[PASS] $name" -ForegroundColor Green }
    else     { $script:FAIL++; Write-Host "[FAIL] $name -> $detail" -ForegroundColor Red }
}

Write-Host "`n=== 1. gcloud instalado e autenticado ===" -ForegroundColor Cyan
$auth = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>&1
Check "gcloud autenticado" ($LASTEXITCODE -eq 0 -and $auth -ne "") "rode: gcloud auth login"

Write-Host "`n=== 2. gcloud config apontando para o projeto certo ===" -ForegroundColor Cyan
$cfgProj = gcloud config get-value project 2>$null
Check "gcloud config project = $PROJ" ($cfgProj -eq $PROJ) "atual: '$cfgProj' -> rode: gcloud config set project $PROJ"

Write-Host "`n=== 3. Variaveis de ambiente (usadas pelo agy) ===" -ForegroundColor Cyan
$envProj = $env:GOOGLE_CLOUD_PROJECT
$envLoc  = $env:GOOGLE_CLOUD_LOCATION
Check "GOOGLE_CLOUD_PROJECT = $PROJ" ($envProj -eq $PROJ) "atual: '$envProj'"
Check "GOOGLE_CLOUD_LOCATION = us-central1" ($envLoc -eq "us-central1") "atual: '$envLoc' (se vazio, feche e reabra o terminal apos o setx)"

Write-Host "`n=== 4. Billing vinculado ao projeto ===" -ForegroundColor Cyan
$billInfo = gcloud billing projects describe $PROJ 2>&1 | Out-String
$billOk = $billInfo -match "billingEnabled: true" -and $billInfo -match [regex]::Escape($BILL)
Check "Billing $BILL habilitado" $billOk "verifique em: console.cloud.google.com/billing/linkedaccount?project=$PROJ"

Write-Host "`n=== 5. API de IA habilitada (Agent Platform / Vertex) ===" -ForegroundColor Cyan
$svc = gcloud services list --enabled --project $PROJ 2>&1 | Out-String
$apiOk = $svc -match "aiplatform.googleapis.com"
Check "aiplatform.googleapis.com habilitada" $apiOk "rode: gcloud services enable aiplatform.googleapis.com --project $PROJ"

Write-Host "`n=== 6. Teste minimo de chamada ao modelo ===" -ForegroundColor Cyan
$testCmd = "gcloud ai models list --project $PROJ --region us-central1"
Write-Host "  (opcional) $testCmd" -ForegroundColor DarkGray
Write-Host "  Se falhar, o agy ainda pode funcionar - o teste real e abrir o agy e rodar 'responda apenas OK'."

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "RESULTADO: $PASS PASS | $FAIL FAIL" -ForegroundColor $(if ($FAIL -eq 0) {"Green"} else {"Yellow"})
Write-Host "============================================`n" -ForegroundColor Cyan