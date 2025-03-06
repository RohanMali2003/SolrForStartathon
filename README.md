# Solr Metadata Connector

A Python utility to extract metadata and sample documents from Apache Solr cores. This tool connects to a Solr instance, retrieves core statistics, and fetches random document samples with their field information.

## Features

- Fetch Solr core metadata (index size, document count)
- Retrieve random document samples
- Extract field types and values
- Generate structured JSON output

## Prerequisites

- Python 3.x
- Apache Solr instance
- Required Python packages:
  ```txt
  requests
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/solr-metadata-connector.git
   cd solr-metadata-connector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create an input file (e.g., `inputs.txt`) with your Solr connection details:

txt
hostname=localhost
portnumber=8983
corename=your_core_name

## Usage

Run the script with your input file as an argument:

bash
python solr_connector.py inputs.txt

The script will generate a `solr_metadata.json` file containing:
- Core metadata (name, size, document count)
- Sample documents with their fields and values

## Output Format

The generated JSON follows this structure:
```json
{
    "type": "apache_solr",
    "data": {
        "CoreName": "core_name",
        "SizeofIndex": 1234,
        "NumberofDocuments": 100,
        "Index": [
            {
                "IndexName": "core_name",
                "Documents": [
                    {
                        "document_id": "id",
                        "fieldTypes": [
                            {
                                "fieldName": "field_name",
                                "value": "field_value"
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

## API Details

The connector interacts with the following Solr APIs:

1. Core Admin API
   - Endpoint: `/solr/admin/cores`
   - Used for retrieving core metadata

2. Search API
   - Endpoint: `/solr/{core}/select`
   - Used for fetching random documents

## Error Handling

The script includes error handling for:
- Invalid input file format
- Missing required configuration
- Failed Solr connection attempts
- Invalid API responses
