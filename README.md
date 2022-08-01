<!--
title: 'AWS Recognition API'
description: 'API for recognition labels on blob files.'
layout: Doc
framework: v3
platform: AWS
language: python
priority: 2
authorLink: 'https://github.com/myauka'
authorName: 'Roman Orlov'
-->


# AWS Recognition API

API for recognition labels on blob files. 

## Usage

API has 2 endpoints:  
POST /blobs - accepts callback_url for receiving callback when recognition will be ended, and return upload_url for uploading pictures.  
GET /blobs/{blob_id} - returns information about recognition results for specified blob.

### Before deployment

Before deployment, you must have installed docker and npm. Npm will be used for plugin installation and this plugin uses docker.  
  
This API includes third-party dependencies. In order to that, you will need to be installed `serverless-python-requirements` plugin. 
  
Installation:

```
$ sls plugin install -n serverless-python-requirements
```
