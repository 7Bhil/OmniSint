import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from core.console import console

def run(phone_number: str):
    console.print(f"[info]Starting Phone OSINT for '{phone_number}'...[/info]")
    results = {"phone_number": phone_number}
    
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number)
        
        # Check if it's a valid number
        is_valid = phonenumbers.is_valid_number(parsed_number)
        results["is_valid"] = is_valid
        
        if not is_valid:
            console.print("[danger][!] The phone number is NOT valid.[/danger]")
            return results
            
        console.print("[success][+] The phone number is VALID.[/success]")
        
        # Get Location
        location = geocoder.description_for_number(parsed_number, "en")
        results["location"] = location
        console.print(f"  [dim]- Location/Region:[/dim] [white]{location or 'Unknown'}[/white]")
        
        # Get Carrier
        service_provider = carrier.name_for_number(parsed_number, "en")
        results["carrier"] = service_provider
        console.print(f"  [dim]- Carrier/ISP:[/dim] [white]{service_provider or 'Unknown'}[/white]")
        
        # Get Timezones
        time_zones = timezone.time_zones_for_number(parsed_number)
        results["time_zones"] = list(time_zones)
        console.print(f"  [dim]- Time Zones:[/dim] [white]{', '.join(time_zones)}[/white]")
        
        # Formats
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        results["national_format"] = national_format
        results["international_format"] = international_format
        console.print(f"  [dim]- National Format:[/dim] [white]{national_format}[/white]")
        console.print(f"  [dim]- International Format:[/dim] [white]{international_format}[/white]")
        
    except phonenumbers.phonenumberutil.NumberParseException as e:
        console.print(f"[danger][!] Parsing Error: {e}[/danger]")
        results["error"] = str(e)
        
    return results
