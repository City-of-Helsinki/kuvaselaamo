# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),


# [3.1.0] 2022-02-10

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
