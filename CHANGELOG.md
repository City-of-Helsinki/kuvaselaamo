# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

# [Unreleased]

### Fixed
- Logos disappearing when user entered shopping cart and checkout views.
- Record details should no longer show extra commas after end of the line.

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
