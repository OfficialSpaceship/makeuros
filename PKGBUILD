# Maintainer: shadow <shadow@localhost>
pkgname=makeuros
pkgver=1.0.9
pkgrel=1
pkgdesc="Customize your Arch Linux system identity (OS name, specs, etc.)"
arch=('any')
url="https://github.com/shadow/makeuros"
license=('MIT')
depends=('python')
source=("makeuros.py")
sha256sums=('SKIP')

package() {
    install -Dm755 "${srcdir}/makeuros.py" "${pkgdir}/usr/bin/makeuros"
}
