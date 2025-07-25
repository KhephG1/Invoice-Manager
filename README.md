Many mistakes were made with this project
 1. The multithreading that allows the UI to run concurrently with the backend logic is bad. The logic needs to ensure long tasks do not block the main thread
 2. Wayyy to many magic numbers. Eg: in the invoice processing logic, the offsets are just hardcoded. This should be changed to be more object oriented.
 3. The way past quantity entries are stored is bad. They are stored in a spreadsheet. They should be stored in a proper sql database.
 4. The program installs a driver for chromium each time it runs which makes it very slow
 5. Should write robust unit tests and integration tests
These issues will be fixed in Invoice manager 2.0! Stay tuned 
