# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

# [3.1.1] 2022-11-08

### Fixed
 - Lowered MAX_RECORDS_PER_FINNA_QUERY from 200 to 150 to avoid a 414 reply from Finna in case
 of a too long request.

# [3.1.0] 2022-11-04

### Added
 - Implements management command to to retrieve id mapping information to a json file and a migration to use the mapping file to update the record ids in the database. Migration needed due to change in the source system and Finna id's.
 - Adds previously removed feedback functionality.
 - Implement minor updates to photo details layout.
 - Replace google analytics with matomo.

### Fixed
 - Fix full resolution image downloads.

# [3.0.0] 2022-02-10

### Fixed
 - Remove leftover JavaScript and CSS related to the already removed buying, ordering and checkout features.
 - Fix JavaScript "load more" functionality
 - Fix browse to last viewed picture in search results
 - Fix changing language removed non-ascii letters from the search terms

# [2.9.0] 2022-01-10

### Changed

 - Increased the memory limit by @nikomakela in #253
 - Removed all the buying, ordering and checkout features by @nikomakela in #252
 - Added the missing accessibility statement code to version control by @nikomakela in #255
 - Update the privacy statement by @nikomakela in #254

# [2.8.1] 2021-12-02

### Fixed

- Fixed an encoding issue when an artist was selected and an image was opened in a gallery.

# [2.8.0] 2021-11-15

### Added

- Reverted the change that removed year and photographer facets. In addition to those added a new facet,
  user is now able to filter images with a year range.

# [2.7.2] 2021-08-24

### Fixed

- Added a type check for getting translation for `image_type`.

# [2.7.1] 2021-08-16

### Changed

- Temporarily disabled single image feedback form. This will be turned back on when background system change is completed.

# [2.7.0] 2021-06-02

### Changed

- Cleaned up the requirements so that the application now has direct dependencies only to those libraries it
  actually uses. Earlier we had quite a lot of unused libraries which were triggering Dependabot alerts and/or
  causing other issues. Now things should be a bit more orderly.
- Updated some libraries to newer versions as suggested by Dependabot.
- Changed the development process to Gitflow. Our staging now gets a new deployment each time `master` gets updated.
  Earlier changes to `develop` were triggering the deployments to staging.

### Removed

- Removed the old printer functionality which was at some point being used in the City Museum premises to print copies
  of images for visitors, but hasn't been in use for a long time. The reason for the removal was that the feature used
  `paramiko` and some other libraries with vulnerabilities, so it was best to get rid of it.

# [2.6.0] 2021-05-25

### Changed

- Replaced any references to Bambora with Visma Pay, as our payment service provider has now rebranded the old Bambora
  service. Replaced the service's banner with the new one.
- Removed all commented out localization file entries to make the files easier to handle.

# [2.5.1] 2021-05-12

### Fixed

- When sending removal notifications via email, a 400 error from Mailgun is now interpreted so that the email
  address is invalid and the user is marked as having been sent the message. This allows the scheduled run to continue
  processing.

# [2.5.0] 2021-05-05

### Added

- Management command which sends email notifications to users whose accounts are going to be removed soon.
- Production environment scheduling for the notification and removal.
- Automated tests for the scheduled commands using pytest.
- Vault configuration in the workflows for handling secrets.
- Automated browser tests which ensure that the main user flows are functioning.

### Changed

- The scheduled cleanup job now waits until 30 days after an email notification has been sent before deleting
  any user data.
- Removed a dummy test which acted as a placeholder.
- Moved some testing related dependencies from requirements.in to requirements-dev.in.

# [2.4.1] 2021-04-01

### Fixed

- Swedish translations in landing page

### Changed

- English translations in landing page

# [2.4.0] 2021-03-17

### Added

- Added script that deletes old and unused data.
- Added kubernetes cron job that executes clean_unused_data script and clearsessions (currently active only in
  staging environment).
- Request a new password functionality.

### Fixed

- Added lang attribute to all collections. It will force screen reader language to finnish.
- Fixed missing title tags to all unique pages.
- If image is not found with image_id, correct error is shown.
- Shopping cart buttons (increase, decrease, delete)
- The shopping basket view now displays images based on the crop selection made by the user.

### Changed

- Moved CGS / Azure dependencies to environment specific requirements.in files.
- Disabled logging for /healthz and /readiness endpoints.

# [2.3.1] 2021-02-01

### Added

- Temporary message stating that feedback processing is congested.

# [2.3.0] 2021-01-12

### Added

- Added lang attribute to language menu.
- Login attempts (success/failure) are now logged.
- Added descriptive names to buttons accross the application.

### Changed

- Add to collection modal no longer shows cropper.

### Fixed

- Error related to missing ios-icon.

# [2.2.0] - 2020-12-21

### Changed

- Remove HEAD query and cache from get_full_res_image_url method.

### Fixed

- When "Load more" is pressed record index counting should start at correct place.
- Fix header layout breaking on Safari.

# [2.1.0] - 2020-12-17

### Added

- Analytics usage may now be switched on/off with an environment variable
- Old-style links to image details are now supported.
- Log configuration is now set up so that it ensures that the extra `data` parameter is present,
  thus allowing for more detailed logging.

### Fixed

- Logos disappearing when user entered shopping cart and checkout views.
- Record details should no longer show extra commas after end of the line.
- Removed extra linefeed symbols from feedback email.
- Fixed "out of index" error that occurred when user was browsing images and last image was reached.
- "Browse albums" view no longer displays duplicate collections when a collection is both
  public and featured
- Language switcher links are now available in the shopping cart views.

### Changed

- Full resolution image is fetched from Finna instead of the proxy server.
- Image details view is now located at `/search/details` so that any old links from search engines or
  other places will get a `404 Not found` from `/search/record`.

## [3.3.0](https://github.com/City-of-Helsinki/kuvaselaamo/compare/kuvaselaamo-v3.2.0...kuvaselaamo-v3.3.0) (2023-11-29)


### Features

* Social media sharing button started ([ac56e2e](https://github.com/City-of-Helsinki/kuvaselaamo/commit/ac56e2e13088c83ffe1ccc1157122d47caff2a1c))


### Bug Fixes

* Add icons ([2dc39dd](https://github.com/City-of-Helsinki/kuvaselaamo/commit/2dc39dd1513b436909a28c63eb1f4e4742770d75))
* Css ([7517594](https://github.com/City-of-Helsinki/kuvaselaamo/commit/75175947540a2cc560c6921f72a55cc2a1b89349))
* Css ([61d7b21](https://github.com/City-of-Helsinki/kuvaselaamo/commit/61d7b21a0276df53cef626c776871e6ca119630b))
* Css ([487702b](https://github.com/City-of-Helsinki/kuvaselaamo/commit/487702bb3c84ae1bdf338942555c850d372be2cd))
* Domain back to twitter ([217ee47](https://github.com/City-of-Helsinki/kuvaselaamo/commit/217ee47da9c55e2a1ca1620a6c8eb67355e5b1c8))
* Encoding ([63752df](https://github.com/City-of-Helsinki/kuvaselaamo/commit/63752df8e5e0725b232c0e38a4832253fbdbdf9b))
* Encoding issues ([07f39e2](https://github.com/City-of-Helsinki/kuvaselaamo/commit/07f39e225ffeef0d1d0e8fb0958dcb23d50a2254))
* Icon class ([f8d1eea](https://github.com/City-of-Helsinki/kuvaselaamo/commit/f8d1eea56553f3d4b52466153229c490b044cdea))
* Js file replace ([d03ccd0](https://github.com/City-of-Helsinki/kuvaselaamo/commit/d03ccd0c38d3b1131f7f638c59ca48dafd7b9af7))
* Link width ([506804b](https://github.com/City-of-Helsinki/kuvaselaamo/commit/506804bfd725ffe6bd4823931a2492a51144f33e))
* Pinterest check description ([ad61e98](https://github.com/City-of-Helsinki/kuvaselaamo/commit/ad61e98e2857257684605b31e34db9cd94ebfc4a))
* Pinterest description ([435985e](https://github.com/City-of-Helsinki/kuvaselaamo/commit/435985eb886c0e8ca4e8ddb3d328df51f89cf1df))
* Pinterest test ([4b28ed7](https://github.com/City-of-Helsinki/kuvaselaamo/commit/4b28ed7c49963515d8dd58ee8e5731eeed34be9a))
* Possible twitter card fix ([b838497](https://github.com/City-of-Helsinki/kuvaselaamo/commit/b838497fc6c2fc6e13a33aecfc1f99aeacde8920))
* Possible twitter fix ([f80ec63](https://github.com/City-of-Helsinki/kuvaselaamo/commit/f80ec63142041abe596af8b8d7fbfebffaa284b6))
* Refactoring matomo logic ([0b55961](https://github.com/City-of-Helsinki/kuvaselaamo/commit/0b55961bf7f6878a515a1d006b89f8371678fe77))
* Remove twitter logo ([22013de](https://github.com/City-of-Helsinki/kuvaselaamo/commit/22013de4dfc9a8c3172c1e68e9d6e93b44ff863d))
* Sharers new tab ([bae6c24](https://github.com/City-of-Helsinki/kuvaselaamo/commit/bae6c24921f88b6232efc31c6da3886c97be2034))
* Test fix for share ([49cf3bd](https://github.com/City-of-Helsinki/kuvaselaamo/commit/49cf3bd16261f6aa1f0da709c396132b9729c2e9))
* Try to update styles and js ([27273a0](https://github.com/City-of-Helsinki/kuvaselaamo/commit/27273a02b92f347e1d5568681772b77054dd78d7))
* Twitter card possible fix ([65c79eb](https://github.com/City-of-Helsinki/kuvaselaamo/commit/65c79ebdee41a365d1fd3e6551cd2c11ef55669b))
* Twitter image to the single details page ([5ae1daa](https://github.com/City-of-Helsinki/kuvaselaamo/commit/5ae1daad67d27e56580a440f3345a33975ab956d))
* Twitter to X ([c13266e](https://github.com/City-of-Helsinki/kuvaselaamo/commit/c13266e066c63f6fb960b16d35f3cae70fa18673))
* Typo ([5b361d0](https://github.com/City-of-Helsinki/kuvaselaamo/commit/5b361d04a085b733149ddd7b1aad3fb3309e6f4e))
* X share ([444d62d](https://github.com/City-of-Helsinki/kuvaselaamo/commit/444d62d6abea29c0ab762643a8563330f92c7c9c))

## [3.2.0](https://github.com/City-of-Helsinki/kuvaselaamo/compare/kuvaselaamo-v3.1.5...kuvaselaamo-v3.2.0) (2023-11-09)


### Features

* Cookie consent started ([ea88f82](https://github.com/City-of-Helsinki/kuvaselaamo/commit/ea88f82208163ddd235c10b0b1f7f64cdda1a3f9))


### Bug Fixes

* Click event1 ([8b6cb91](https://github.com/City-of-Helsinki/kuvaselaamo/commit/8b6cb91ba5e8e914daacc036e53b4e380b24dd4c))
* Cookie consent footer navi link ([cba8a80](https://github.com/City-of-Helsinki/kuvaselaamo/commit/cba8a8054620c270cbd4b696ecefc5da830b2831))
* Cookie consent implementation ([ad7b383](https://github.com/City-of-Helsinki/kuvaselaamo/commit/ad7b3835d7965d104b281c08e470566645a65e70))
* Mobile view scroll auto ([c6e7927](https://github.com/City-of-Helsinki/kuvaselaamo/commit/c6e7927c2f8add9fd3f15e9c684aa783314cc2af))
* Refactoring and updating the translations ([d81018e](https://github.com/City-of-Helsinki/kuvaselaamo/commit/d81018eaa34a8cfcb02824fd13427dada8ae4e4e))
* Remove paddings from cookie consent ([92a9992](https://github.com/City-of-Helsinki/kuvaselaamo/commit/92a9992816e368efd1b33c5164d264fc82a05410))
* Table overflow ([14c87e1](https://github.com/City-of-Helsinki/kuvaselaamo/commit/14c87e1c214bae9f91558c8f27a2ba3b395122e6))
* Translations ([6e3fd17](https://github.com/City-of-Helsinki/kuvaselaamo/commit/6e3fd17fd634587a483173cf873ce387c041b3c6))
* Translations changes ([92a8d33](https://github.com/City-of-Helsinki/kuvaselaamo/commit/92a8d33a7aaec08fc3848a47bed99075a90cf4f3))
* Typo consent js ([30387b1](https://github.com/City-of-Helsinki/kuvaselaamo/commit/30387b16f587c61606c2715bafed9f2e8c18405e))

## [3.1.5](https://github.com/City-of-Helsinki/kuvaselaamo/compare/kuvaselaamo-v3.1.4...kuvaselaamo-v3.1.5) (2023-10-10)


### Bug Fixes

* Load more bug fix ([79e185f](https://github.com/City-of-Helsinki/kuvaselaamo/commit/79e185f60d87cdf724914614378d394b42ed79bf))
* Too small image in preview ([011f897](https://github.com/City-of-Helsinki/kuvaselaamo/commit/011f8970b779f5fa9076d4c8e2bf79dd773e82bd))
* Use smaller thumbnails ([c198ebe](https://github.com/City-of-Helsinki/kuvaselaamo/commit/c198ebe2875867f37b891449d6aa48d7caf2be53))

## [3.1.4](https://github.com/City-of-Helsinki/kuvaselaamo/compare/kuvaselaamo-v3.1.3...kuvaselaamo-v3.1.4) (2023-09-05)


### Bug Fixes

* Force ci browser tests locale to en-US ([d27ae7f](https://github.com/City-of-Helsinki/kuvaselaamo/commit/d27ae7f047b865ef8ba60b1e189b2814d3039c2c))
* Force test language using app feature ([c71f1cd](https://github.com/City-of-Helsinki/kuvaselaamo/commit/c71f1cd6960d78917fe5be49cea01d72eec05e03))
* Populate photo details cache ([146eac0](https://github.com/City-of-Helsinki/kuvaselaamo/commit/146eac0ba411c4e00610c1baa71162941351bf29))
* Release-please configurations HEL-341 ([533f7e9](https://github.com/City-of-Helsinki/kuvaselaamo/commit/533f7e9b7b0fadf7574daf77f391aff761b4d4b3))
* Use original photo for downloads only ([9441093](https://github.com/City-of-Helsinki/kuvaselaamo/commit/9441093a7ddbfa185c77c23aa59740da308d17dd))
* Use thumbnail images in photo lists ([c51c8e7](https://github.com/City-of-Helsinki/kuvaselaamo/commit/c51c8e715fe516269d0623146b0bd08fb36e0a6a))

## [2.0.1] - 2020-12-09

### Fixed

- Fixed issue where using scandinavian letters on search would crash the application.

## [2.0.0] - 2020-12-08

### Added

- Configurations for running the application using Docker and Kubernetes in the new Culture and Leisure
  environment, including Gitlab configurations for running the CI/CD pipeline.
- New functionality for showcasing selected collections on the front page.
- Image details now display the address where the image was taken (this data is available via Finna API).

### Changed

- Image files will no longer be stored in the local filesystem. Instead they are stored in cloud storage (GCS or
  Azure, depending on the environment).
- Email notifications are sent using the Mailgun service.
- Lots of layout changes, including front page hero area, header, footer, image browsing views etc
- "Add to album" functionality no longer fetches two copies of the image to the local filesystem.
- "Download full resolution image" link now points directly to the full res image on the proxy server instead of the
  local copy.
- "Share image" functionality is removed.
- Search view's author/year filters have been removed.

### Fixed

- Search functionality's results now use URLs which do not depend on the index of the previous Finna search result.
- Performance fixes for various image browsing views (repeating SQL queries removed).
- Image detail view's buttons may now be used with a mobile device.
