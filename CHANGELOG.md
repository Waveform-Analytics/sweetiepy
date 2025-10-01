# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-10-01

### Fixed
- **CRITICAL TIMEZONE FIX**: Fixed systematic 4-hour timestamp offset in treatment data
  - Treatment timestamps were stored as local time but marked with UTC timezone indicators
  - This caused visualization and analysis tools to display treatments 4 hours off from actual times
  - Added `_fix_corrupted_treatment_timestamps()` helper function to handle the correction transparently
  - Added comprehensive documentation about the timezone corruption issue and its root causes
  - The fix maintains compatibility with both corrupted and properly stored data

### Added
- Added `pytz>=2024.1` dependency for timezone handling
- Added detailed documentation about timezone data corruption in MongoDB
- Added warning messages when timezone correction is applied

### Technical Details
- Root cause: DIY Loop system or data ingestion pipeline storing Eastern time values with 'Z' (UTC) suffixes
- Impact: All treatment data (boluses, basal changes, carb corrections) appeared 4 hours offset from actual times
- Solution: Detect UTC-marked timestamps that are actually local time and correct them transparently
- Affected methods: `get_dataframe_for_period()`, `get_treatments()`, and all derived methods

This fix is essential for accurate data analysis and visualization of diabetes treatment data.

## [1.0.0] - 2025-09-30

### Added
- Initial release of SweetiePy
- CGM data access and analysis
- Pump treatment data integration  
- Merged CGM and pump settings analysis
- Time-in-range calculations
- Settings correlation analysis
- MongoDB Atlas connectivity
- High-performance PyArrow backend
- Comprehensive documentation and examples