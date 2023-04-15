# Changelog

All notable changes to this project will be documented in this file.

The format is inspired on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased
### Changed
- Readers are now independent tasks. Instead of having a File task that uses
readers we have a ReadCsv task, a ReadJson task... One per each format. This
removes a lot of complexity.


## 1.0.0a1 - 02-03-2023
### Added
- Loading files relative to the configuration file.
- Adding `mnemocards_anki.Pronounce`: task for pronouncing text using Google
Translator.
- Adding more docs.


## 1.0.0a0 - 06-03-2023
A complete rewrite of the mnemocards package. Some features are missing.
