#!/bin/bash

echo "=== Cognitive Services Soft-Deleted Resources Cleanup ==="
echo

# Function to list soft-deleted resources
list_deleted_resources() {
    echo "Listing all soft-deleted Cognitive Services accounts..."
    echo
    
    # Check if there are any deleted accounts
    deleted_count=$(az cognitiveservices account list-deleted --output json | jq '. | length')
    
    if [ "$deleted_count" -eq 0 ]; then
        echo "No soft-deleted Cognitive Services accounts found."
        return 1
    fi
    
    echo "Found $deleted_count soft-deleted account(s):"
    echo
    
    # Display the accounts in a nice table format
    printf "%-30s %-20s %-30s\n" "Name" "Location" "ResourceGroup"
    printf "%-30s %-20s %-30s\n" "----" "--------" "-------------"
    az cognitiveservices account list-deleted --output json | \
        jq -r '.[] | "\(.name)\t\(.location)\t\(.id | split("/")[8])"' | \
        while IFS=$'\t' read -r name location resource_group; do
            printf "%-30s %-20s %-30s\n" "$name" "$location" "$resource_group"
        done
    
    return 0
}

# Function to purge all soft-deleted resources
purge_all_deleted_resources() {
    echo
    echo "Purging all soft-deleted Cognitive Services accounts..."
    echo
    
    # Get the list of deleted accounts as JSON
    deleted_accounts=$(az cognitiveservices account list-deleted --output json)
    
    # Check if there are any accounts to purge
    if [ "$(echo "$deleted_accounts" | jq '. | length')" -eq 0 ]; then
        echo "No accounts to purge."
        return 0
    fi
    
    # Loop through each deleted account and purge it
    echo "$deleted_accounts" | jq -r '.[] | "\(.name)\t\(.location)\t\(.id | split("/")[8])"' | \
    while IFS=$'\t' read -r name location resource_group; do
        echo "Purging: $name in $location (Resource Group: $resource_group)"
        
        # Purge the account
        if az cognitiveservices account purge \
            --location "$location" \
            --resource-group "$resource_group" \
            --name "$name" --output none 2>/dev/null; then
            echo "  ✓ Successfully purged $name"
        else
            echo "  ✗ Failed to purge $name"
        fi
    done
    
    echo
    echo "Purge operations completed."
}

# Function to verify cleanup
verify_cleanup() {
    echo
    echo "Verifying cleanup..."
    
    remaining_count=$(az cognitiveservices account list-deleted --output json | jq '. | length')
    
    if [ "$remaining_count" -eq 0 ]; then
        echo "✓ All soft-deleted accounts have been successfully purged."
    else
        echo "⚠ Warning: $remaining_count account(s) still remain in soft-deleted state."
        echo "They may take a few moments to be fully purged."
    fi
}

# Main execution
main() {
    # List the resources first
    if list_deleted_resources; then
        echo
        read -p "Do you want to purge all these soft-deleted accounts? (y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            purge_all_deleted_resources
            verify_cleanup
        else
            echo "Operation cancelled."
        fi
    fi
    
    echo
    echo "Script completed."
}

# Check if running with --force flag to skip confirmation
if [ "$1" = "--force" ] || [ "$1" = "-f" ]; then
    echo "Force mode enabled - purging without confirmation..."
    if list_deleted_resources; then
        purge_all_deleted_resources
        verify_cleanup
    fi
else
    main
fi
