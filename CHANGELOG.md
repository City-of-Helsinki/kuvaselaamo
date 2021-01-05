# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

# [Unreleased]
### Added
- Added lang attribute to language menu.
- Login attempts (success/failure) are now logged.

### Changed
- Add to collection modal no longer shows cropper.

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
