# Saer setup and operations

[← Project overview](../README.md) · [Delivery and presentation](../DELIVERY.md)

This guide covers the **locally verified Windows CPU runtime**. Cloudflare Pages serves the static interface and historical data; it does not execute Python or the models. No publicly connected model service is currently verified.

## 1. Prerequisites and scope

| Requirement | Tested reference |
|---|---|
| Operating system | Windows x64 |
| Python | 3.12.10, with the Python launcher available as `py -3.12` |
| Frontend tools | Node 24.22.1 · pnpm 11.25.0 |
| Hardware | CPU, 16 GB RAM |
| Storage | Allow roughly 10–15 GiB for the two environments, encoder weights, and caches |
| Network | Needed for initial package installation and public encoder restoration |
| Repository | Normal authorized GitHub access while the repository remains private |

The CPU locks have not been validated on Linux, macOS, or Kaggle/GPU. Historical verification used package caches and a declared, checksum-verified encoder cache. A complete package-and-weight download on another cache-free machine remains untested. These limits are recorded in the [reproducibility report](PHASE4_REPRODUCIBILITY.md).

Use a separate checkout or extracted delivery copy. Keep the approved deployment directory and original datasets untouched. No training is required.

## 2. Run the historical-data interface

From a fresh checkout:

```powershell
git clone https://github.com/rayan18q-bot/saer.git
cd saer
pnpm --dir frontend install --frozen-lockfile
Copy-Item frontend/.env.example frontend/.env.local
pnpm --dir frontend dev
```

Open **http://127.0.0.1:5173** and choose guest access. The template enables `VITE_DEMO_MODE=true`: browsing, filtering, comparison, recommendations, and descriptive analysis use historical JSON exports. Model requests use a separately configured Gradio service.

For an existing checkout, preserve any existing `frontend/.env.local` instead of overwriting it. The template is a starting point, not a place for secrets.

### Build and preview

Inside `frontend/`:

```powershell
pnpm exec tsc --noEmit
$env:VITE_DEMO_MODE='true'
pnpm build
pnpm preview --port 5194
```

The static demo output is `frontend/dist-demo`; preview is **http://127.0.0.1:5194**. Building does not publish it, and the generated directory is not part of Git. Never run this build inside the approved deployment copy.

Without demo mode, the application uses the REST `/api` path and Vite's local proxy configuration, producing the other build output. That mode needs its own integration check; it is not a substitute for the verified demo-mode flow. Build success alone does not establish functional completeness.

## 3. Create two independent Python environments

Run from the **repository root**, in PowerShell:

```powershell
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:SAER_IMAGE_PYTHONPATH -ErrorAction SilentlyContinue
$env:PYTHONNOUSERSITE='1'
py -3.12 -m venv .runtime/clean-main
py -3.12 -m venv .runtime/clean-image
.runtime/clean-main/Scripts/python.exe -m pip install -r requirements-runtime-lock.txt
.runtime/clean-image/Scripts/python.exe -m pip install -r requirements-image-lock.txt
.runtime/clean-main/Scripts/python.exe -m pip check
.runtime/clean-image/Scripts/python.exe -m pip check
.runtime/clean-main/Scripts/python.exe tools/check_runtime_env.py
.runtime/clean-image/Scripts/python.exe tools/check_runtime_env.py --image
```

The lockfiles include the direct and transitive versions from the independently installed environments. The corresponding `requirements-runtime.txt` and `requirements-image.txt` contain the direct dependency specifications used to create those locks. Package sources are PyPI and the official PyTorch CPU wheel index.

| Environment | scikit-learn | Torch / torchvision | Used for |
|---|---|---|---|
| `.runtime/clean-main` | 1.9.1 | 2.14.1+cpu / 0.29.1+cpu | Specification pricing, identity, REST, and Gradio |
| `.runtime/clean-image` | 1.6.1 | 2.5.1+cpu / 0.20.1+cpu | Image-price worker only |

Both use Transformers 4.45.2, NumPy 2.5.3, Pandas 2.3.3, and Pillow 11.3.0. Gradio is 5.49.1, with Python client 1.13.3 in the main environment.

**Do not combine the environments.** The saved image-price artifact requires its training-time scikit-learn version. The worker runs through `SAER_IMAGE_PYTHON`; a mismatch fails explicitly rather than returning a replacement result. Do not use `PYTHONPATH`, `--system-site-packages`, or packages borrowed from another project. The environment checker verifies that imports originate inside the selected venv and that user-site packages are disabled.

## 4. Restore public encoders

The three small approved artifacts are already included: **5,916,575 bytes total**. Their embedded preprocessing, class maps, pointers, and required project code are part of the delivery. See [runtime-assets.json](runtime-assets.json).

They do not include all pretrained feature extractors. Restore the declared public files before starting the image paths:

```powershell
.runtime/clean-main/Scripts/python.exe tools/restore_public_encoders.py --download
.runtime/clean-main/Scripts/python.exe tools/restore_public_encoders.py
```

The first command downloads **missing files only**, validates their sizes and SHA-256 hashes, and refuses to replace an existing mismatched file. The second verifies the existing cache without downloading. No token is required for these public sources.

The inventory contains **15 weight/configuration files, about 2.72 GiB**, plus the pinned DINOv2 source. It covers DINOv2 ViT-S/B/L, CLIP ViT-B/16 and ViT-B/32, ResNet18, and SSDLite support weights. Exact sources, revisions, files, and hashes:

- [Public encoder guide](PUBLIC_ENCODERS.md)
- [Machine-readable inventory](PUBLIC_ENCODERS.json)

The current identity code reads the user's default home cache:

| Files | Location relative to `Path.home()` |
|---|---|
| CLIP snapshots | `.cache/huggingface/hub/` |
| DINOv2 source and Torch checkpoints | `.cache/torch/hub/` |

Do not assume that changing `HF_HOME` or `TORCH_HOME` relocates every runtime path. The restore tool's `--home` option is for restoration testing; it does not change where the current model code reads assets.

The existing 15 files and 157 DINOv2 Python source files were verified. Restoring the pinned DINOv2 source into an empty test directory was also verified. A complete re-download of all large weights, interrupted-download recovery, and every remote source with a missing local file were not retested.

**For a presentation:** restore in advance, run the verification-only command before the session, and do not add `--download` during the demonstration.

## 5. Start a local model service

In a separate terminal at the repository root:

```powershell
./tools/start_runtime.ps1 -Mode gradio
```

Gradio listens at **http://127.0.0.1:7863**. The script checks both Python executables and the public cache, sets the repository asset roots and image worker, disables user-site/PYTHONPATH imports, enables offline Hugging Face access, and limits CPU threads.

Keep the frontend running in its own terminal, then open:

**http://127.0.0.1:5173/?api=http%3A%2F%2F127.0.0.1%3A7863**

The API query is stored in sessionStorage for that browser-tab session. A fresh session without a configured API should show the Arabic missing-service message when estimation is requested. An unreachable service should report an error and leave no substitute prediction.

### REST alternative

```powershell
./tools/start_runtime.ps1 -Mode rest
```

REST listens at **http://127.0.0.1:8000**. Health is available at `/api/health`; the three verification endpoints are `/api/estimate-tabular`, `/api/recognize`, and `/api/estimate-image-price`. SQLite is initialized from the selected data tables. A healthy endpoint alone does not prove that inference works.

Both startup modes bind to loopback. They do not create a public tunnel or alter hosting settings. Do not run two expensive inference jobs concurrently on a 16 GB machine.

### Manual startup and a fresh result cache

If PowerShell script execution is unavailable, use the Python commands directly instead of weakening machine-wide policy. First verify encoders as in section 4. Then set the explicit environment below; it also provides a **new result cache** for a live verification run:

```powershell
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:SAER_IMAGE_PYTHONPATH -ErrorAction SilentlyContinue
$env:PYTHONNOUSERSITE='1'
$env:PYTHONIOENCODING='utf-8'
$env:SAER_APP_ROOT=(Get-Location).Path
$env:LOCAL_ASSETS_DIR=(Get-Location).Path
$env:SAER_IMAGE_PYTHON=(Resolve-Path .runtime/clean-image/Scripts/python.exe).Path
$env:SAER_RUNTIME_CACHE=Join-Path (Get-Location) ('.runtime-cache/demo-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
$env:HF_HUB_OFFLINE='1'
$env:TRANSFORMERS_OFFLINE='1'
$env:OMP_NUM_THREADS='4'
$env:MKL_NUM_THREADS='4'
$env:FRONTEND_ORIGINS='http://127.0.0.1:5173,https://saer-rmsavg637.pages.dev'
.runtime/clean-main/Scripts/python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

To start Gradio manually instead, use the same explicit environment and replace the last line with:

```powershell
.runtime/clean-main/Scripts/python.exe -m uvicorn app:app --app-dir hf_backend --host 127.0.0.1 --port 7863
```

For a frontend preview on port 5194, explicitly add `http://127.0.0.1:5194` to `FRONTEND_ORIGINS` before starting Gradio. This changes only the local server's allowed origins.

## 6. Verify actual inference

With the REST service running against a **fresh cache**, open a second terminal at the repository root:

```powershell
$env:PYTHONPATH=$null
$env:PYTHONNOUSERSITE='1'
$env:PYTHONIOENCODING='utf-8'
$reportPath=Join-Path (Get-Location) ('.runtime/verification-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.json')
.runtime/clean-main/Scripts/python.exe tools/verify_delivery_runtime.py --output $reportPath
```

This makes real HTTP requests for the three models, checks the artifact hashes, and requires the image and identity responses to report a cache miss. A successful run writes a new evidence report. It does not supply prices to the UI from saved JSON. To repeat a fresh inference run, restart with another result-cache directory; preserve previous evidence.

The runtime predicts on the included `frontend/public/demo/img/sample-1186/04.webp`. The image-price API accepts up to eight photos of the same car; the standalone image-price screen currently uses the **first selected image only**. Multi-image runtime paths have not received the same end-to-end verification as the single-photo sample.

For frontend behavior checks, without model training:

```powershell
node --test tests/frontend-behavior.mjs
```

Existing evidence and its limits are recorded in [the unification verification](UNIFICATION_VERIFICATION.json), [phase 5 verification](PHASE5_VERIFICATION.json), and [frontend validation](FRONTEND_FIX_VALIDATION.md). Their dates and scopes matter; they are not blanket accuracy claims.

## 7. Environment reference

| Variable | Purpose / behavior |
|---|---|
| `SAER_APP_ROOT`, `LOCAL_ASSETS_DIR` | Repository root containing the code and small model artifacts; set by the startup script |
| `SAER_IMAGE_PYTHON` | Absolute executable path for the separate image-price worker |
| `SAER_RUNTIME_CACHE` | Writable result cache and REST SQLite location; select a new path for cache-miss verification |
| `FRONTEND_ORIGINS` | Comma-separated allowed CORS origins; the script defaults to local port 5173 and the current published site |
| `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` | Set to 1 after restoring all required encoder files |
| `OMP_NUM_THREADS`, `MKL_NUM_THREADS` | CPU limits; the launcher uses 4 |
| `PYTHONNOUSERSITE` | Set to 1; avoid implicit user-site dependencies |
| `VITE_DEMO_MODE` | `true` for historical JSON data and the static demo build |
| `VITE_GRADIO_SPACE_URL` or `?api=` | Gradio URL; a loopback address is useful only to the local browser |
| `VITE_API_BASE_URL` | Compatibility fallback used by the frontend API configuration resolver |
| `VITE_API_CONFIG_URL` or `?apiConfig=` | Optional public JSON/Gist configuration source for the API URL; not configured in the delivery |

The root `.env.example` is illustrative. Python does not automatically load it. Export variables in PowerShell or supply them through the hosting environment. Do not put credentials in `VITE_*` variables: they are shipped to the browser. Private-asset recovery options in `model_store.py` remain for other workflows; they are unnecessary with the bundled approved artifacts.

Never commit real `.env` files, tokens, virtual environments, public encoder caches, raw photos, or generated builds. The restore command for the public assets above requires no token.

## 8. Dataset, provenance, and permissions

The delivery contains 2,742 historical advertisements, 13,416 image records, and one original dataset photo linked to `demo-1186`. The other photo files are deferred. A record, filename, or original image count does not establish that the underlying file is bundled. The local demo uses placeholders for most listings.

The existing public deployment includes a different asset snapshot, including photos already published there. Do not treat that as proof that the Git snapshot contains them, and do not copy the complete image collection into Git without verifying sharing permissions. See [sample image scope](SAMPLE_IMAGES.md) and [data contract](../DATA_CONTRACT.md).

The Cairo font retains its [OFL license](../frontend/public/fonts/OFL.txt). Some design and vehicle imagery have unresolved provenance or redistribution rights. Keep their existing notices and do not infer blanket permission from academic use. No repository-wide MIT or other software license is asserted.

The image-price artifact's recorded upstream repository, commit, and retrospective evaluation are preserved in [its pointer](../models/image_price_current.json). The joint make/model head is the active identity model; older standalone-make diagnostics are not an extra live UI model. [ML_SPEC.md](../ML_SPEC.md) contains historical proposals as well as later decisions; the README's model table is based on the saved runtime artifacts.

## 9. Delivery backup and recovery

Create a new ZIP **outside the repository**, from a clean committed state:

```powershell
$backupZip=Join-Path (Split-Path (Get-Location) -Parent) 'saer-delivery.zip'
py -3.12 tools/package_delivery.py --output $backupZip
```

The packager refuses an existing destination and includes only committed Git files plus `VERSION.txt`. It verifies CRC, the tracked-file manifest, byte-for-byte content, and forbidden paths/secret patterns, then writes a SHA-256 sidecar. It does not include virtual environments, caches, the full image dataset, or large public encoders.

To restore: check the sidecar hash, extract to a **new directory**, inspect `VERSION.txt` for the exact commit, then follow sections 2–5. The encoder restore instructions remain inside the ZIP. Existing delivery ZIPs are immutable snapshots; a later documentation commit does not silently update them. Source heads, recovery paths, branch history, and historical hashes are maintained in [DELIVERY.md](../DELIVERY.md) and [PROGRESS.md](../PROGRESS.md).

## 10. Hosting and legacy notebook scope

The known Cloudflare project uses Direct Upload and has no Git provider attached. At unification, repository workflows and webhooks were checked and none were present. No automatic deployment was enabled or performed. Read current settings again before any future hosting change; a historical audit does not guarantee future configuration.

No approved public model endpoint is currently configured and verified. Local inference is not a public-site inference test. A separately authorized HTTPS service and browser CORS verification would be needed for that next step.

`notebooks/kaggle_server.ipynb` and `tools/package_kaggle.py` remain as an earlier alternative workflow. The latter creates a private backend bundle; neither establishes that the notebook, GPU runtime, or public tunnel currently works. The present lockfiles describe the tested CPU environment. Do not place tokens in notebook cells, frontend variables, or Git; no Kaggle/GPU setup is needed for the local route above.

## Troubleshooting

| Symptom | Check |
|---|---|
| Estimation shows the Arabic missing-service message | Start Gradio and open the local frontend with the `?api=` URL above |
| Service is unreachable | Confirm the local process and port; do not replace the error with saved prices |
| Image worker reports a scikit-learn mismatch | Use the separate 1.6.1 worker and its explicit `SAER_IMAGE_PYTHON` |
| Public encoder verification fails | Restore missing files before the presentation; inspect mismatched files rather than overwriting them |
| Verification reports a cached response | Stop REST and restart with a new `SAER_RUNTIME_CACHE` |
| Frontend preview has a CORS error | Include its exact origin, including port, in the local Gradio allowlist |
| Most local advertisements show a placeholder | Expected: only one original dataset photo is bundled |
| A launch script cannot run | Use the documented manual Python startup; no machine-wide policy change is required |
