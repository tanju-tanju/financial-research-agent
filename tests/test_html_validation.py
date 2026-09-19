#!/usr/bin/env python3
import sys

def check_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    if '</html>' not in content:
        errors.append("Missing </html>")
    if '</script>' not in content:
        errors.append("Missing </script>")
    if 'Sparda' in content or 'sparda' in content:
        errors.append("Forbidden word 'Sparda' found in index.html!")
    
    # Check key pipeline elements
    required_ids = [
        'pipelineDropZone',
        'pipelineCountBadge',
        'presetSelect',
        'pipelineEditorArea',
        'pipelineStepPromptInput',
        'btnPipelineExecute',
        'pipelineProgressBarContainer',
        'pipelineResultsNavigator',
        'pipelineResultStepPills',
        'containerStep3',
        'stepBtnTrailer',
        'trailerVideoPlayer',
        'trailerHeaderTitle'
    ]
    for rid in required_ids:
        if f'id="{rid}"' not in content:
            errors.append(f"Missing required element id='{rid}'")

    if errors:
        print("Validation FAILED:", errors)
        sys.exit(1)
    else:
        print("Validation SUCCESS: index.html is valid, completely purged of Sparda, and contains all pipeline elements.")

if __name__ == '__main__':
    check_html()
