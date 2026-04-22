# BR2 local web launcher

Web nay gom 2 che do:

1. `Local launcher`: chay file `BR2\BR2_thichlaviet.com.exe` qua web noi bo.
2. `Khong can exe`: mo truc tiep trang `https://thichlaviet.com/` bang giao dien web tinh.

## Cau truc

```text
.
|-- BR2/
|   |-- BR2_thichlaviet.com.exe
|   |-- thichlaviet.com.URL
|   `-- README.md
|-- launcher_web/
|   |-- app.py
|   `-- index.html
|-- index.html
|-- start_web.ps1
`-- README.md
```

## Cach 1: chay local launcher

Yeu cau:

- Windows
- Python 3
- File `BR2\BR2_thichlaviet.com.exe` nam dung thu muc

Chay:

```powershell
.\start_web.ps1
```

Neu Windows hien hop thoai UAC, bam `Yes`.

Sau do mo:

```text
http://127.0.0.1:8000
```

Tren web co 2 nut:

- `Chay file`: mo `BR2_thichlaviet.com.exe`
- `Mo website goc`: mo thang `https://thichlaviet.com/`

## Cach 2: khong can exe

Mo file [index.html](/abs/path/c:/Users/User/OneDrive/Desktop/BR2/index.html) bang trinh duyet, hoac dua file nay len hosting/GitHub Pages.

Trang nay khong can Python va khong can `.exe`. No chi lam 2 viec:

- mo website goc
- thu mo local launcher tai `http://127.0.0.1:8000` neu ban da chay server

## Luu y

- Trinh duyet khong the tu chay `.exe` truc tiep. Muon bam nut de mo `.exe`, bat buoc phai qua local Python server.
- File `.exe` hien khong nam trong ban upload GitHub. Neu clone repo ve, ban can tu dat lai file nay vao thu muc `BR2\`.
- Neu nut `Chay file` bao loi quyen admin, hay chay lai `.\start_web.ps1` va chap nhan hop thoai UAC.

## Dua len mang

### GitHub Pages

Repo da duoc them san:

- `.nojekyll`
- workflow `.github/workflows/deploy-pages.yml`

URL du kien:

```text
https://dybinh2k5.github.io/BR2-local-web-launcher/
```

Neu GitHub Pages chua tu publish, vao:

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

Sau do workflow se tu deploy moi lan push len `main`.

Neu ban muon van dung `GitHub Actions` nhung khong muon tu tay bat Pages truoc, tao secret repository:

```text
Settings -> Secrets and variables -> Actions -> New repository secret
```

Ten secret:

```text
PAGES_PAT
```

Gia tri secret:

- Personal Access Token cua GitHub
- can co quyen `repo` hoac it nhat quyen Pages write

Workflow da duoc sua de:

- neu co `PAGES_PAT`: thu tu enable Pages bang GitHub Actions
- neu khong co `PAGES_PAT`: dung flow mac dinh, can bat Pages thu cong 1 lan trong Settings

### Vercel

Repo da co `.vercelignore` de chi deploy web tinh.

Can dang nhap 1 lan tren may cua ban:

```powershell
vercel login
vercel --prod
```
