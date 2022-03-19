# Performant

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

## Running and deploying:

### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
