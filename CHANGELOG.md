# Change Log

This document records all notable changes to fnpdjango.

## 0.4.5 (2020-03-26)

- Support for Django up do 3.0.
- Added `actions.export_as_csv_action`.


## 0.4.3 (2019-10-02)

- Make textile import optional when loading template tags.


## 0.4.1 (2019-09-27)

- Make `utils.settings.LazyUGettextLazy` a `django.utils.functional.Promise`
  so it deconstructs nicely.


## 0.4 (2019-04-03)

- Support for Django up to 2.2.
- `textile` and `pipeline` dependencies are now in extras.
- Deprecated `utils.urls.i18n_patterns` and `middleware.URLLocaleMiddleware`,
  as Django 1.10 adds `prefix_default_language` parameter to `i18n_patterns`.
- Removed `auth_backends.AttrCASBackend`; use `django-cas-ng` instead.
- Added this changelog.


## 0.3 (2019-02-15)

- Support for Django 1.11.
- Dropped support for Python 2.6, 3.2, 3.3
- Removed `prefix` parameter from `utilsurls.i18n_patterns`.


## 0.2.8 (2018-07-10)

- Restored `utils.text.char_map`, removed in 0.2 with `slughifi`.


## 0.2.7 (2018-01-22)

- Enabled `auto_link` in `utils.text.textilepl.textile_restricted_pl`.


## 0.2.6 (2017-07-25)

- Added `utils.fields.TextfileField`.


## 0.2.4 (2017-04-05)

- Support for Django 1.10
- Removed nk.pl from share icons.
- Updated textile.


## 0.2.3 (2017-02-14)

- Fixed import for Django 1.9


## 0.2.2 (2016-11-08)

- Fixed bad HTTP 404 in `middleware.URLLocaleMiddleware`.


## 0.2.1 (2016-01-04)

- Test with Django up to 1.9.


## 0.2 (2014-09-30)

- Removed `utils.text.slughifi`; use `python-slugify` instead.
- Removed deployment scripts to another package (`fnpdeploy`).
- Added tests.


## 0.1.19-1 (2014-09-01)

- Pinned textile version.


## 0.1.19 (2014-06-09)

- `auth_backends.AttrCASBackend`: Save user instance only when necessary.
- `deploy`: Added `migrate_fake` option.
- `deploy`: Added root `manage.py` helper script.


## 0.1.18 (2014-03-31)

- Added `templatetags.fnp_annoy`.


## 0.1.17 (2014-03-27)

- Added `auth_backends.AttrCASBackend`.


## 0.1.16 (2014-02-25)

- Added `utils.pipeline_storage.GzipPipelineCachedStorage`.


## 0.1.15 (2014-02-14)

- Added `storage.BofhFileSystemStorage`.


## 0.1.14 (2014-01-14)

- `deploy`: Fixed gunicorn sample upload when `django_root_path` not set.


## 0.1.13 (2014-01-14)

- Enable styling language switcher link depending on the destination language.


## 0.1.12 (2014-01-02)

- `deploy`: Added git hash to relase name.


## 0.1.11 (2013-12-30)

- Support Django 1.6
- Minor fixes in deployment and bootstrap scripts.


## 0.1.10 (2013-12-12)

- `deploy`: Added `skip_collect_static` option.


## 0.1.9.1 (2013-12-06)

- Quick fix for textile.


## 0.1.9 (2013-12-06)

- Added `templatetags.fnp_markup.textile_en` and `textile_restricted_en`.


## 0.1.8 (2013-11-19)

- Fixed unicode check in slughifi.
- Fixes for deployment and bootstrap scripts.


# 0.1.7 (2013-07-04)

- Fix packaging for `makecontribmessages` command.

Changes in `deploy`:
- Added `Command` task.
- Added `pre_collectstatic` hook.
- Added `django_root_path` and `localsettings_dst_path` options.
- Auto-install DB requirements.
- Made `setup` idempotent.
- Upgrade `git-archive-all.sh` script.
- Set `SECRET_KEY` on setup.
- Various minor fixes.


## 0.1.6 (2013-03-20)
- Support for Django 1.5


## 0.1.5-1 (2013-02-22)

- Quick fix for previous page link in prevnext.


## 0.1.5 (2013-02-22)

- Made prevnext respect current GET parameters.
- Added a management command for localizing contrib apps.
- Fixed deployment sudo problem.


## 0.1.4 (2013-01-10)

- Added tQ function for filtering translated fields.


## 0.1.3 (2013-01-09)

- Fixedd `get_here_url`.
- Nicer project starter.
- Fixed deployment scripts.


## 0.1.2 (2012-11-30)

- Added app settings.
- Fixed deployment scripts.
- Minor fixes.


## 0.1.1 (2012-11-22)

- Added deployment scripts.
- Minor fixes.


## 0.1 (2012-11-05)

- Initial release.
