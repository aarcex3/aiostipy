# Change log

## 05/08/2024

### Changed

- Controllers are classes with prefix
- Route are simple functions, they become RouteDef in the Application class

### Added

- opyoid as dependecy injector
- mgspec as json encoder and decoder
- uvloop as asyncio event loop

### Removed

- poetry.lock

### Fix

- Now the app runs AND accepts requests
