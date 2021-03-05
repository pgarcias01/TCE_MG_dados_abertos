# TCE_MG_dados_abertos

## Crawler to download, extract and organize all data from <a href="https://dadosabertos.tce.mg.gov.br/view/xhtml/paginas/downloadArquivos.xhtml" target="_blank">TCE-MG</a>

## Getting started

1. Setting configs in config.json

* driver_path : path where selenium browser located
* link : link of page where data of TCE-MG
* max_process : number of multi-process crawler do
* parent_dir : directory where saved the folders

2. Run crawler

```
cd src
python app.py
```
