# Performant User Interface

The UI was created with the Angular framework.

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.2.2.

## Pages:

- Summary
    - All of the overall account summary information.
- Visualize
    - Graphical visualizations (over time) of account / stock metrics
- History
    - Tabular view of the stock summary
- Input
    - User component for inserting new stock purchases / sales.
- Account
    - Account management, such as funding accounts.

## Important Components:

- navbar
    - The unified navigation between pages.
- api-service
    - The HTTP client which sends and receives API requests

## Important Notes:
1. Currently, there is some validation (on forms) but there is little standardization and typechecking as that would take extra time to implement.
2. The application itself is also incredibly brittle, more time is required to add robustness. For instance, stock transactions are required before navigating to the home page.
   1. Easily fixable by adding a check, but lower on the priority list vs pure functionality.
3. API Information is stored in the environment files. If you have a different backend, these may be helpful to change.

## Running and deploying:

The application while being developed was run completely on the local development server.

### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.
