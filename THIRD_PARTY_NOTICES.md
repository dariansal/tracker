# Third-party notices

The app code in this repository is MIT licensed (see `LICENSE`). These bundled components are included under their own terms:

| File | Component | License |
|---|---|---|
| `assets/ocr-core.js` | [tesseract.js-core](https://github.com/naptha/tesseract.js-core) 5.1.1 (`tesseract-core-lstm.wasm.js`), a WebAssembly build of the Tesseract OCR engine | Apache License 2.0. Full text in `assets/LICENSE-tesseract.js-core` |
| `assets/ocr-eng-data.js` | English language data for Tesseract (`eng.traineddata`, best_int), from the npm package [@tesseract.js-data/eng](https://www.npmjs.com/package/@tesseract.js-data/eng) 1.0.0, gzipped and base64-encoded | Package: MIT. Original data: Tesseract OCR project, Apache License 2.0 |
| `assets/usda-foods.js` | Nutrient values and portion weights derived from the USDA National Nutrient Database for Standard Reference, Release 28 (via the npm package fda-nutrient-database 1.0.2) | USDA data: U.S. government work, public domain. Package: MIT |

No changes were made to the Tesseract engine. The English data was only compressed and encoded. The USDA data was reduced to name, calories, protein, carbohydrate, fat, and cup and whole-item weights.
