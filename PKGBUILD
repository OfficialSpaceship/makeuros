# Maintainer: shadow <shadow@localhost>
pkgname=makeuros
pkgver=1.0.24
pkgrel=1
pkgdesc="Customize your Arch Linux system identity and setup Docker containers for 19 self-hosted services"
arch=('any')
url="https://github.com/OfficialSpaceship/makeuros"
license=('MIT')
depends=('python')
source=("makeuros.py::https://github.com/OfficialSpaceship/makeuros/raw/V${pkgver}/makeuros.py")
sha256sums=('SKIP')

package() {
    install -Dm755 "${srcdir}/makeuros.py" "${pkgdir}/usr/bin/makeuros"
}
