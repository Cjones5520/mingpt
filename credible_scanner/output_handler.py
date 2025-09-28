"""
Output handler for saving signature scan results to Excel spreadsheets.

Uses pandas to organize extracted data into structured format.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


def prepare_results_data(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Prepare results data for Excel output.
    
    Args:
        results (List[Dict[str, Any]]): List of scan results
        
    Returns:
        pd.DataFrame: Prepared DataFrame for Excel export
    """
    rows = []
    
    for result in results:
        file_path = result.get('file_path', '')
        file_name = Path(file_path).name if file_path else 'Unknown'
        form_type = result.get('form_type', 'Unknown')
        total_pages = result.get('total_pages', 0)
        signatures_found = result.get('signatures_found', 0)
        error = result.get('error', '')
        
        signature_locations = result.get('signature_locations', [])
        
        if not signature_locations:
            # Add a row even if no signatures found
            rows.append({
                'File Name': file_name,
                'File Path': file_path,
                'Form Type': form_type,
                'Total Pages': total_pages,
                'Signatures Found': signatures_found,
                'Page Number': '',
                'Signature Type': '',
                'X Coordinate': '',
                'Y Coordinate': '',
                'Width': '',
                'Height': '',
                'Confidence': '',
                'Error': error,
                'Scan Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            # Add a row for each signature location
            for sig in signature_locations:
                rows.append({
                    'File Name': file_name,
                    'File Path': file_path,
                    'Form Type': form_type,
                    'Total Pages': total_pages,
                    'Signatures Found': signatures_found,
                    'Page Number': sig.get('page', ''),
                    'Signature Type': sig.get('type', ''),
                    'X Coordinate': sig.get('x', ''),
                    'Y Coordinate': sig.get('y', ''),
                    'Width': sig.get('width', ''),
                    'Height': sig.get('height', ''),
                    'Confidence': sig.get('confidence', ''),
                    'Error': error,
                    'Scan Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return pd.DataFrame(rows)


def create_summary_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary sheet with aggregate statistics.
    
    Args:
        df (pd.DataFrame): Main results DataFrame
        
    Returns:
        pd.DataFrame: Summary DataFrame
    """
    summary_data = []
    
    # Overall statistics
    total_files = df['File Name'].nunique()
    total_signatures = df[df['Signature Type'] != '']['Signature Type'].count()
    files_with_signatures = df[df['Signatures Found'] > 0]['File Name'].nunique()
    files_with_errors = df[df['Error'] != '']['File Name'].nunique()
    
    summary_data.append({
        'Metric': 'Total Files Processed',
        'Value': total_files
    })
    summary_data.append({
        'Metric': 'Total Signatures Found',
        'Value': total_signatures
    })
    summary_data.append({
        'Metric': 'Files with Signatures',
        'Value': files_with_signatures
    })
    summary_data.append({
        'Metric': 'Files with Errors',
        'Value': files_with_errors
    })
    summary_data.append({
        'Metric': 'Success Rate (%)',
        'Value': round((files_with_signatures / total_files * 100), 2) if total_files > 0 else 0
    })
    
    # Form type breakdown
    form_types = df.groupby('Form Type')['File Name'].nunique().reset_index()
    form_types.columns = ['Metric', 'Value']
    form_types['Metric'] = 'Form Type: ' + form_types['Metric'].astype(str)
    
    # Signature type breakdown
    sig_types = df[df['Signature Type'] != ''].groupby('Signature Type').size().reset_index()
    sig_types.columns = ['Metric', 'Value']
    sig_types['Metric'] = 'Signature Type: ' + sig_types['Metric'].astype(str)
    
    # Combine all summary data
    summary_df = pd.DataFrame(summary_data)
    form_types_df = pd.DataFrame(form_types)
    sig_types_df = pd.DataFrame(sig_types)
    
    return pd.concat([summary_df, form_types_df, sig_types_df], ignore_index=True)


def save_results(
    results: List[Dict[str, Any]], 
    output_file: str = "signature_scan_results.xlsx"
) -> str:
    """
    Save signature scan results to an Excel file.
    
    Args:
        results (List[Dict[str, Any]]): List of scan results
        output_file (str): Output Excel file name
        
    Returns:
        str: Path to the saved file
    """
    # Prepare data
    df = prepare_results_data(results)
    summary_df = create_summary_sheet(df)
    
    # Create Excel writer
    output_path = os.path.abspath(output_file)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write main results
        df.to_excel(writer, sheet_name='Signature Scan Results', index=False)
        
        # Write summary
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    return output_path


def save_debug_info(
    results: List[Dict[str, Any]], 
    debug_file: str = "signature_scan_debug.txt"
) -> str:
    """
    Save detailed debug information to a text file.
    
    Args:
        results (List[Dict[str, Any]]): List of scan results
        debug_file (str): Debug output file name
        
    Returns:
        str: Path to the saved debug file
    """
    debug_path = os.path.abspath(debug_file)
    
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(f"Credible PDF Signature Scanner - Debug Log\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"File {i}: {result.get('file_path', 'Unknown')}\n")
            f.write(f"Form Type: {result.get('form_type', 'Unknown')}\n")
            f.write(f"Total Pages: {result.get('total_pages', 0)}\n")
            f.write(f"Signatures Found: {result.get('signatures_found', 0)}\n")
            
            if result.get('error'):
                f.write(f"Error: {result['error']}\n")
            
            signature_locations = result.get('signature_locations', [])
            if signature_locations:
                f.write("Signature Locations:\n")
                for j, sig in enumerate(signature_locations, 1):
                    f.write(f"  {j}. Page {sig.get('page', '?')}: "
                           f"Type={sig.get('type', '?')}, "
                           f"Pos=({sig.get('x', '?')},{sig.get('y', '?')}), "
                           f"Size={sig.get('width', '?')}x{sig.get('height', '?')}, "
                           f"Confidence={sig.get('confidence', '?')}\n")
            
            f.write("-" * 40 + "\n\n")
    
    return debug_path


def export_csv(
    results: List[Dict[str, Any]], 
    csv_file: str = "signature_scan_results.csv"
) -> str:
    """
    Export results to CSV format for compatibility.
    
    Args:
        results (List[Dict[str, Any]]): List of scan results
        csv_file (str): CSV output file name
        
    Returns:
        str: Path to the saved CSV file
    """
    df = prepare_results_data(results)
    csv_path = os.path.abspath(csv_file)
    df.to_csv(csv_path, index=False)
    return csv_path