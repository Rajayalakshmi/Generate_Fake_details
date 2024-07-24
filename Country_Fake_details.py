from faker import Faker
import warnings

# Predefined dataset for states and zip codes
predefined_data = {
    'Germany': {'state': 'Bavaria', 'zipcode': '80331'},
    'Japan': {'state': 'Tokyo', 'zipcode': '100-0001'},
    'Spain': {'state': 'Madrid', 'zipcode': '28001'},
    'France': {'state': 'Île-de-France', 'zipcode': '75001'},
    'India': {'state': 'Maharashtra', 'zipcode': '400001'},
    # Add more predefined data as needed
}

def generate_fake_details(locale, country):
    fake = Faker(locale)
    country_details = {}
    try:
        country_details["first_name"] = fake.first_name()
    except AttributeError:
        country_details["first_name"] = "N/A"
    
    try:
        country_details["last_name"] = fake.last_name()
    except AttributeError:
        country_details["last_name"] = "N/A"
    
    try:
        country_details["full_name"] = fake.name()
    except AttributeError:
        country_details["full_name"] = "N/A"
    
    try:
        country_details["address"] = fake.address()
    except AttributeError:
        country_details["address"] = "N/A"
    
    try:
        if hasattr(fake, 'postalcode'):
            country_details["zip_code"] = fake.postalcode()
        elif hasattr(fake, 'zipcode'):
            country_details["zip_code"] = fake.zipcode()
        else:
            country_details["zip_code"] = predefined_data.get(country, {}).get('zipcode', 'N/A')
    except AttributeError:
        country_details["zip_code"] = predefined_data.get(country, {}).get('zipcode', 'N/A')
    
    try:
        country_details["city"] = fake.city()
    except AttributeError:
        country_details["city"] = "N/A"
    
    try:
        country_details["state"] = fake.state() if hasattr(fake, 'state') else predefined_data.get(country, {}).get('state', 'N/A')
    except AttributeError:
        country_details["state"] = predefined_data.get(country, {}).get('state', 'N/A')
    
    return country_details

# Dictionary mapping country names to their locales
country_locale_map = {
    'United States': 'en_US',
    'Canada': 'en_CA',
    'Germany': 'de_DE',
    'Japan': 'ja_JP',
    'Spain': 'es_ES',
    'France': 'fr_FR',
    'India': 'en_IN',
    'Italy': 'it_IT',
    'Brazil': 'pt_BR',
    'China': 'zh_CN',
    'Russia': 'ru_RU',
    'Mexico': 'es_MX',
    'South Korea': 'ko_KR',
    'Australia': 'en_AU',
    'Netherlands': 'nl_NL',
    'Turkey': 'tr_TR',
    'Sweden': 'sv_SE',
    'Argentina': 'es_AR',
    'Chile': 'es_CL',
    'Colombia': 'es_CO',
    'Egypt': 'ar_EG',
    'Greece': 'el_GR',
    'Hungary': 'hu_HU',
    'Indonesia': 'id_ID',
    'Ireland': 'en_IE',
    'Israel': 'he_IL',
    'Malaysia': 'ms_MY',
    'New Zealand': 'en_NZ',
    'Norway': 'no_NO',
    'Poland': 'pl_PL',
    'Portugal': 'pt_PT',
    'Romania': 'ro_RO',
    'Singapore': 'en_SG',
    'Slovakia': 'sk_SK',
    'Switzerland': 'de_CH',
    'Thailand': 'th_TH',
    'Ukraine': 'uk_UA',
    'United Arab Emirates': 'ar_AE',
    'United Kingdom': 'en_GB',
    'Vietnam': 'vi_VN',
    'Pakistan': 'en_PK',
    'Bangladesh': 'en_BD',
    'Philippines': 'en_PH',
    'Nigeria': 'en_NG',
    'Kenya': 'en_KE',
    'Belgium': 'nl_BE',
    'Austria': 'de_AT',
    'Czech Republic': 'cs_CZ',
    'Denmark': 'da_DK',
    'Finland': 'fi_FI',
    'Hong Kong': 'zh_HK',
}

# Filter out invalid locales
valid_country_locale_map = {}
for country, locale in country_locale_map.items():
    try:
        Faker(locale)
        valid_country_locale_map[country] = locale
    except AttributeError:
        print(f"Skipping invalid locale for {country}: {locale}")

# Generate fake details for each valid country
fake_details_map = {}
for country, locale in valid_country_locale_map.items():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        details = generate_fake_details(locale, country)
        if details:
            fake_details_map[country] = details

# Display the list of countries to the user
print("Supported countries:")
for country in fake_details_map.keys():
    print(country)

# Ask the user to input a country name
user_country = input("\nEnter the name of the country you want to see fake details for: ").strip()

# Clean up any extra characters from the input
user_country = user_country.split('&')[0].strip()

# Display fake details for the selected country
if user_country in fake_details_map:
    print(f"\nFake details for {user_country}:")
    details = fake_details_map[user_country]
    for key, value in details.items():
        print(f"{key}: {value}")
    print("\n" + "-"*50 + "\n")
else:
    print(f"Country {user_country} is not supported.")
