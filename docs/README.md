# EzyGallery Documentation

This project is a simple Flask showcase for the EzyGallery MVP. A light and dark theme can be toggled via the button in the page header. The selected theme is stored in the browser and reapplied on next visit.

For development there is an optional cache busting system. Toggle it by visiting `/toggle-nocache`. When enabled, static asset URLs will include a timestamp query parameter so browsers always fetch the latest files.
