import os
import shutil

def rename_files():
    base_dir = os.path.join(os.getcwd(), "EXHIBITS")
    
    # Mapping: "Old Filename (lowercase)" -> "New Filename"
    mapping = {
        # Exhibit A
        "leave of absence - us.pdf": "Exhibit A - Leave of Absence Policy.pdf",
        "u.s. employee handbook.pdf": "Exhibit A - Employee Handbook.pdf",
        "terminations.pdf": "Exhibit A - Termination Policy.pdf",
        "vestas personnel guide.pdf": "Exhibit A - Personnel Guide.pdf",
        "attendance.pdf": "Exhibit A - Attendance Policy.pdf",
        "performance management_corrective action.pdf": "Exhibit A - Performance Management Policy.pdf",
        "us non-exempt (hourly) pto.pdf": "Exhibit A - Hourly PTO Policy.pdf",

        # Exhibit B
        "exhibit b_ financial strangulation timeline.pdf": "Exhibit B - Financial Strangulation Timeline.pdf",

        # Exhibit C
        "ada2_transcript.pdf": "Exhibit C - July 17 Transcript.pdf",

        # Exhibit D
        "svp_lopez_ticket_closure.pdf": "Exhibit D - Executive Ratification (Lopez Closure).pdf",

        # Exhibit E
        "formal_complaint.pdf": "Exhibit E - Formal Complaint (Objection).pdf",

        # Exhibit F
        "06_payment details _ my famli+.pdf": "Exhibit F - JAMLI Payment Details (Benefit Exhaustion).pdf",
        "bomb_threat.pdf": "Exhibit F - Culture Evidence (Bomb Threat).pdf",
        "250722_claudio_hostile_email.pdf": "Exhibit F - Hostile Email (Claudio).pdf",
        "250804_final_impasse_email.pdf": "Exhibit F - Final Impasse Email.pdf",
        "250717_interactive_meeting_summary.pdf": "Exhibit F - Interactive Meeting Summary.pdf",
        
        # Exhibit G
        "unum_payment_.pdf": "Exhibit G - Bad Faith (UNUM Payment).pdf",

        # Exhibit H
        "exhibit_h-1_diagnostic_summary_(self-extracted).pdf": "Exhibit H-1 - Diagnostic Summary.pdf",
        "records - as .pdf": "Exhibit H - Full Medical Records (Private).pdf",

        # Exhibit J
        "exhibit-j-3-affidavit.pdf": "Exhibit J-3 - Affidavit (Scheurer).pdf",
        "exhibit_j-5_flsa__colorado_wage_law_exposure_calculation.pdf": "Exhibit J-5 - Exposure Calculation.pdf",

        # Exhibit K
        "01_section_232_looming_tariffs.pdf": "Exhibit K - Context (Section 232 Tariffs).pdf",
        "01_section_232_mcguirewoods.pdf": "Exhibit K - Context (McGuireWoods Analysis).pdf",
        "02_ftz_colorado_sun_article.pdf": "Exhibit K - Context (FTZ Article).pdf",
        "02_ftz_compliance_guide_2025.pdf": "Exhibit K - Context (FTZ Compliance Guide).pdf",
        "02_ftz_vestas_authorization.pdf": "Exhibit K - Context (FTZ Authorization).pdf",
        "03_ira_baker_donelson.pdf": "Exhibit K - Context (IRA Baker Donelson).pdf",
        "03_ira_prevailing_wage_reqs.pdf": "Exhibit K - Context (IRA Prevailing Wage).pdf",

        # Exhibit M
        "exhibit-m-financial-strangulation-system.pdf": "Exhibit M - Financial Strangulation System.pdf"
    }

    print("Starting renaming process...")
    count = 0 
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            lower_name = file.lower()
            if lower_name in mapping:
                old_path = os.path.join(root, file)
                new_name = mapping[lower_name]
                new_path = os.path.join(root, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed:\n  {file}\n  -> {new_name}")
                    count += 1
                except Exception as e:
                    print(f"Error renaming {file}: {e}")

    print(f"\nRenaming complete. {count} files renamed.")

if __name__ == "__main__":
    rename_files()
