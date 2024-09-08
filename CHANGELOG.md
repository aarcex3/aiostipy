# Change log

## 08/09/2024

## Refactor

- Parameters

### Remove

- **`aiohttp_extracts` integration**: Forked the original repo and fixed somes bugs

## 22/08/2024

### Added

- **`aiohttp_extracts` integration**: Added support for parameter extraction using `aiohttp_extracts`. This improves handling of request parameters and enhances the overall flexibility of the framework.
- **Parameter Types**: Introduced new parameter types for request handling:
  - `Header`
  - `Query`
  - `Param`
  - `Cookie`
  - `File`
  - These parameters provide more granular control over request data extraction and improve the ease of defining endpoints.
- **Response Types**: Introduced new response classes:
  - `JSONResponse` (using `msgspec`)
  - `ORJSONResponse`
  - `HTMLResponse`
  - `RedirectResponse`
  - These responses improve content handling and response formatting for various use cases.
  By default all response are JSONResponse.

### Improved

- **Parameter Extraction**: Imported and adapted `fetch_fn_params` from `aiohttp_extract` to suit the current use case, ensuring more efficient and consistent parameter extraction.
- **Controller Class Defaults**: The `Controller` class now includes a default route prefix (`/`), simplifying route definitions and minimizing the need for redundant configuration.
- **Service Class Scope**: The `Service` class is now set with a default scope (`SingletonScope`), promoting better resource management and optimizing service lifecycles.
- **File Parameter Handling**: Implemented support for the `File` parameter type, leveraging the `aiohttp_extract` library. This allows seamless file handling in requests.

### Removed

- Cli folder. It's a seperate project -> [aiostipy-cli](https://github.com/aarcex3/aiostipy-cli)

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
