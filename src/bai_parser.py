import csv
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from BAI_BOA import bai_code_descriptions  # Import BAI codes from external file

class BAIParser:
    def __init__(self):
        self.current_account = ""
        self.current_date = None
        self.current_aba = ""
        self.records = []
        self.bai_code_descriptions = bai_code_descriptions
        self.logger = logging.getLogger(__name__)

    def parse_file(self, content: str) -> List[Dict]:
        lines = content.split('\n')
        
        for line in lines:
            if not line.strip() or line.startswith('<'):
                continue
                
            fields = [f.strip() for f in line.split(',')]
            record_code = fields[0]
            
            self.logger.debug(f"Processing line: {line}")
            self.logger.debug(f"Record code: {record_code}")
            
            if record_code == '02':  # Group Header Record
                if len(fields) >= 5:
                    # Get routing number from field 3
                    self.current_aba = fields[2]
                    self.logger.debug(f"Set ABA routing number to: {self.current_aba}")
                    
                    # Parse date from field 5 (YYMMDD format)
                    date_str = fields[4]
                    self.logger.debug(f"Found group header date: {date_str}")
                    try:
                        self.current_date = datetime.strptime(date_str, '%y%m%d')
                        self.logger.debug(f"Parsed group date: {self.current_date}")
                    except ValueError as e:
                        self.logger.error(f"Failed to parse group date: {e}")
                        self.current_date = None
                        
            elif record_code == '03':  # Account Identifier
                self.current_account = fields[1]
                self.logger.debug(f"Set account: {self.current_account}")
                
            elif record_code == '88':  # Summary Record
                self._process_transaction(fields)
        
        return self.records

    def _process_transaction(self, fields: List[str]) -> None:
        """Process a transaction record."""
        self.logger.debug(f"Processing transaction: {fields}")
        
        if len(fields) < 3:
            self.logger.warning("Invalid transaction record: insufficient fields")
            return

        try:
            # Get BAI code
            bai_code = fields[1].strip()
            
            # Convert amount from cents to dollars
            amount = float(fields[2]) / 100 if fields[2].strip() else 0.0
            
            # Get count and funds type
            count = fields[3].strip() if len(fields) > 3 and fields[3].strip().isdigit() else ""
            funds_type = fields[4].split('/')[0].strip() if len(fields) > 4 else 'Z'
            
            record = {
                'DateField': self.current_date.strftime('%m/%d/%Y') if self.current_date else '',
                'ABA_RoutingField': f'"{self.current_aba}"',  # Explicit double quotes
                'AccountField': f'"{self.current_account}"',   # Explicit double quotes
                'BAI_Code': bai_code,
                'BAI_Description': f'"{self.bai_code_descriptions.get(bai_code, "")}"',  # Explicit double quotes
                'Amount': f"${amount:.2f}",
                'Count': count,
                'Funds_Type': funds_type
            }
            
            self.logger.debug(f"Created record: {record}")
            self.records.append(record)
            
        except Exception as e:
            self.logger.error(f"Error processing record: {e}")
            self.logger.error(f"Fields: {fields}")
            
            self.logger.debug(f"Created record: {record}")
            self.records.append(record)
            
        except Exception as e:
            self.logger.error(f"Error processing record: {e}")
            self.logger.error(f"Fields: {fields}")

    def write_csv(self, output_file: str) -> None:
        if not self.records:
            return

        fieldnames = [
            'DateField', 'ABA_RoutingField', 'AccountField', 
            'BAI_Code', 'BAI_Description', 'Amount',
            'Count', 'Funds_Type'
        ]

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, 
                fieldnames=fieldnames,
                quoting=csv.QUOTE_NONE,  # Don't add any additional quotes
                quotechar=None,
                escapechar=None
            )
            writer.writeheader()
            writer.writerows(self.records)
            self.logger.info(f"Wrote {len(self.records)} records to {output_file}")

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Define input and output folders
    input_folder = Path("input")
    output_folder = Path("output")
    
    logger.debug(f"Input folder path: {input_folder}")
    logger.debug(f"Output folder path: {output_folder}")
    
    # Check if input folder exists and is a directory
    if not input_folder.exists():
        print(f"Error: Input folder '{input_folder}' does not exist")
        return 1
    if not input_folder.is_dir():
        print(f"Error: '{input_folder}' is not a directory")
        return 1
    
    # Create output folder if it doesn't exist
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created or verified output folder: {output_folder}")
    except Exception as e:
        print(f"Error creating output folder: {str(e)}")
        return 1
    
    # Get list of .bai files
    bai_files = list(input_folder.glob('*.bai'))
    logger.debug(f"Found BAI files: {[f.name for f in bai_files]}")
    
    if not bai_files:
        print(f"No .bai files found in {input_folder}")
        return 1
    
    total_files = 0
    total_records = 0
    
    for bai_file in bai_files:
        try:
            logger.debug(f"Processing file: {bai_file}")
            
            # Create output CSV filename with same base name
            output_file = output_folder / f"{bai_file.stem}.csv"
            logger.debug(f"Output file will be: {output_file}")
            
            with open(bai_file, 'r', encoding='utf-8') as file:
                bai_content = file.read()
                logger.debug(f"Successfully read file content, length: {len(bai_content)}")
            
            bai_parser = BAIParser()
            records = bai_parser.parse_file(bai_content)
            
            if records:
                bai_parser.write_csv(str(output_file))
                total_files += 1
                total_records += len(records)
                print(f"\nProcessed file {bai_file.name}:")
                print(f"- Output file: {output_file}")
                print(f"- Records processed: {len(records)}")
            else:
                logger.warning(f"No records found in {bai_file.name}")
            
        except Exception as e:
            logger.exception(f"Error processing file {bai_file}")
            print(f"Error processing file {bai_file}: {str(e)}")
            continue
    
    print(f"\nProcessing complete:")
    print(f"- Total files processed: {total_files}")
    print(f"- Total records processed: {total_records}")
    print(f"- Output folder: {output_folder}")
    
    return 0 if total_files > 0 else 1

if __name__ == "__main__":
    exit(main())