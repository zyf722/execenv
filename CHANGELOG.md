# CHANGELOG

## v0.1.1 (2024-09-04)

### Chore

* chore: update README.md with badges ([`87296d8`](https://github.com/zyf722/execenv/commit/87296d86413878c87e4ad9cc75307217bfd4865d))

* chore: add code quality check tools as dev dependencies ([`ad6c99b`](https://github.com/zyf722/execenv/commit/ad6c99b5b1656813916a8e9a6b889ffd2bc2bd26))

* chore: ignore missing import ([`f48df32`](https://github.com/zyf722/execenv/commit/f48df32328c6318698d47815a7cac135482fe2bb))

* chore: add `py.typed` marker ([`7286960`](https://github.com/zyf722/execenv/commit/7286960f89e50c6990113ef42d6bc22948366f56))

* chore: add Codecov badge to README.md ([`27f7957`](https://github.com/zyf722/execenv/commit/27f7957b73cc56f9bb027ca1f7434aeb08f76d07))

* chore(dep): add pytest-cov ([`d195d2b`](https://github.com/zyf722/execenv/commit/d195d2bd5bfd7b32411db58f9fcb32da16477d97))

* chore: update build workflow to include changes to build.yml ([`f9919a1`](https://github.com/zyf722/execenv/commit/f9919a1ecddbcde2288438224e2ff1a4c82703d2))

* chore: add vscode workspace settings ([`4750953`](https://github.com/zyf722/execenv/commit/475095377056a06e23d8e91393be5164682f6fb0))

* chore: update README ([`9dd6579`](https://github.com/zyf722/execenv/commit/9dd6579ba57fde476d21cb4f2cd18a05e9881057))

* chore: update README ([`a448f5b`](https://github.com/zyf722/execenv/commit/a448f5b7a9af4b6d8e23200924463de3bc1e9bc6))

* chore: update screenshot for execenv-completion ([`594d70b`](https://github.com/zyf722/execenv/commit/594d70b5c2de5d3c498381d2690387fdcee323ae))

* chore: update README ([`19f24eb`](https://github.com/zyf722/execenv/commit/19f24ebaedb1488b03b124219dde84f0540bed3d))

* chore: update README ([`69f0a3d`](https://github.com/zyf722/execenv/commit/69f0a3d46ef4bce86c78651d6ad436fb419ed54a))

* chore: update README ([`160118d`](https://github.com/zyf722/execenv/commit/160118d31be9f51647811518b4b3b8a1b8e233f4))

### Ci

* ci: update build workflow name ([`905f9d5`](https://github.com/zyf722/execenv/commit/905f9d55dfccb68d275edd627e4d66f5afa9b810))

* ci: add manual semantic release action ([`6e590e7`](https://github.com/zyf722/execenv/commit/6e590e7188fdff14a8653fbe25c09997a4c088ff))

* ci: update Codecov configuration and workflow ([`fabec0d`](https://github.com/zyf722/execenv/commit/fabec0d43f3b99fd1420782dce0c2c7feab8efc8))

* ci: add ruff, isort and mypy for code quality check ([`93567cd`](https://github.com/zyf722/execenv/commit/93567cd7539adf0c12ae9464201428963aa584bd))

* ci: move typos check to common check ([`bc3f11c`](https://github.com/zyf722/execenv/commit/bc3f11c62f9905b8ffd109a88a2d1c81c3a3e356))

* ci: codecov integration ([`b46d82f`](https://github.com/zyf722/execenv/commit/b46d82f442a9b76cfc86ba37e4c7c18684d7caef))

* ci: update build workflow to exclude typos check on Windows ([`4428f9e`](https://github.com/zyf722/execenv/commit/4428f9edd878749934e576f73736f19801fb0d6d))

* ci: install wget for typos on Windows ([`5241e30`](https://github.com/zyf722/execenv/commit/5241e3007af2f20b2a352ca2c3d2569b7915b41c))

* ci: run build when tests changes ([`b430a04`](https://github.com/zyf722/execenv/commit/b430a0421ad7cca0f3da06e543cf48230367692a))

* ci: add tests ([`84324a2`](https://github.com/zyf722/execenv/commit/84324a2698992ae857f6f6d5f2a02c0e88c1d2d4))

### Fix

* fix(ci): update build workflow to include coverage report ([`adf3800`](https://github.com/zyf722/execenv/commit/adf38007e606e83bd505cbf19cc9c0db28730eeb))

* fix(test): fix test for `-c` ([`62f1d72`](https://github.com/zyf722/execenv/commit/62f1d72fbe645a9d22de98ab44796813569910ac))

* fix: change test mode into env var ([`e4f3874`](https://github.com/zyf722/execenv/commit/e4f387486d91fa6fd4aa68cc37d898af7998a5f8))

* fix: handle OSError when getting terminal size ([`3ebc932`](https://github.com/zyf722/execenv/commit/3ebc93279ebf794d62df5b68aa80af68ae505dd8))

* fix: fix typo that disabling version ([`32ca02a`](https://github.com/zyf722/execenv/commit/32ca02ab4686e28b8717c3a8b1068ca886d6298d))

* fix: remove multiple call typo ([`31e2eeb`](https://github.com/zyf722/execenv/commit/31e2eeb663dc9415d3819658db08a227ab7119ba))

### Refactor

* refactor: use `poetry run` for `execenv-echo` ([`05f8703`](https://github.com/zyf722/execenv/commit/05f87031bda1577152ecc4b67bc599ca65526a92))

* refactor: enable click shell completion only if not in test mode ([`cbe937f`](https://github.com/zyf722/execenv/commit/cbe937fe6c63dbbfd15b29d9df735f2345122287))

* refactor: improve assert error message in `CliTestResult` ([`df998bc`](https://github.com/zyf722/execenv/commit/df998bcdc30427bf10ae16dd1921d64e52716656))

* refactor: separate `get_shell_env_varref_format` for future use ([`21fd1e5`](https://github.com/zyf722/execenv/commit/21fd1e52896b0d5a2fcea8120b00d99af1dd6866))

* refactor: switch from `print` to `click.echo` ([`e6c12ad`](https://github.com/zyf722/execenv/commit/e6c12ade26b5d25e7cfe30268c42a127af2ec818))

### Test

* test: use pytest-xdist to speed up testing ([`8e34156`](https://github.com/zyf722/execenv/commit/8e3415614b540efb66fa4d259ade93194a1f452f))

* test: add pytest ([`f096b59`](https://github.com/zyf722/execenv/commit/f096b5908d424fcac9162cd44203ea7234b558f2))

## v0.1.0 (2024-08-17)

### Chore

* chore: add -V / --version for execenv-echo ([`307f934`](https://github.com/zyf722/execenv/commit/307f93454d2f9bcc49dd3a44c07bff32d6cf2bc5))

* chore: update README ([`ae3ea52`](https://github.com/zyf722/execenv/commit/ae3ea528b0a66c042a054816e533f41ad91861a6))

* chore: update README ([`7ee25d3`](https://github.com/zyf722/execenv/commit/7ee25d30afed593d95b14119c30f94674366457d))

* chore: add assets using git lfs ([`9dd6dbf`](https://github.com/zyf722/execenv/commit/9dd6dbf0e92a1a81493264ca720db8d997aa4f6f))

* chore: update metadata ([`aa4ebe4`](https://github.com/zyf722/execenv/commit/aa4ebe4fef3f1a42fd32f7b72c0c432adcdc8d36))

* chore: add LICENSE ([`4c44708`](https://github.com/zyf722/execenv/commit/4c4470888a37ce6cbce2bd70947069b234a0bc6e))

* chore: add .gitignore ([`dd7ed83`](https://github.com/zyf722/execenv/commit/dd7ed83fa1cfa2e2fd1dbf8a7878959b431776bc))

* chore: add clink completion ([`6027fc5`](https://github.com/zyf722/execenv/commit/6027fc598674806dcddf7c30e61d840aeaa18ee8))

* chore: add metadata ([`fa2654a`](https://github.com/zyf722/execenv/commit/fa2654ad3c035d75236d8ddd3e441d23436eb1ce))

### Ci

* ci: only run when source changes ([`3171532`](https://github.com/zyf722/execenv/commit/3171532049d3d8a658e3c5f05ce8f51954d0cc5f))

* ci: add github actions ci ([`6ce279b`](https://github.com/zyf722/execenv/commit/6ce279b96b084960bed63c37e526d3c936cfc63b))

### Feature

* feat: add auto completion for -h / -V / --help / --version ([`9d7534e`](https://github.com/zyf722/execenv/commit/9d7534e359deaaaf456d64aac464c8b1cd3e195a))

* feat: fix bugs and overhaul ([`4cbe599`](https://github.com/zyf722/execenv/commit/4cbe59941d9f0ed7e2b2a9b0480bc0f72f73e5e0))

* feat: add execenv-completion ([`1d21784`](https://github.com/zyf722/execenv/commit/1d21784d3eb497f191c47ec65a8e61aa9cf30a06))

* feat: tab completion support ([`81bccb6`](https://github.com/zyf722/execenv/commit/81bccb647d2ee78e79f77a47209fbee048bb7b2c))

* feat: initial commit ([`dfc88a3`](https://github.com/zyf722/execenv/commit/dfc88a329b1a31c10f285eae6010082336ae522e))

### Fix

* fix(ci): use `python-path` for poetry env as X.Y not working on windows (python-poetry/poetry#2117) ([`93f5afe`](https://github.com/zyf722/execenv/commit/93f5afe876c4b1c2054ffc493fac190880e00a12))

* fix(ci): use str to reference version correctly ([`a691148`](https://github.com/zyf722/execenv/commit/a69114849190110a3252f77d20269062d50aebf7))

* fix: backwards compatible typing ([`16faf82`](https://github.com/zyf722/execenv/commit/16faf82baf049fd83e15a094f7e7be5a6282ec90))

### Refactor

* refactor: use builtin `ReprHighlighter` of rich ([`abe47fa`](https://github.com/zyf722/execenv/commit/abe47fa2d41e52c502f47e20df53013b85104b5a))
