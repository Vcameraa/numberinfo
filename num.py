# phone_info.py
import requests
import sys
import os
import json

# কনফিগারেশন ফাইল পাথ
CONFIG_FILE = "phone_info_config.json"

def load_config():
    """কনফিগারেশন লোড করুন বা নতুন তৈরি করুন"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # নতুন কনফিগারেশন তৈরি করুন
    config = {
        "api_key": "",
        "api_provider": "apilayer"  # apilayer বা abstractapi
    }
    save_config(config)
    return config

def save_config(config):
    """কনফিগারেশন সেভ করুন"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def set_api_key():
    """API Key সেট করুন"""
    config = load_config()
    
    if config["api_key"]:
        print(f"\nবর্তমান API Key: {config['api_key']}")
        print(f"বর্তমান API প্রোভাইডার: {config['api_provider']}")
        change = input("\nআপনি কি API Key পরিবর্তন করতে চান? (y/n): ").lower()
        if change != 'y':
            return
    
    print("\n" + "="*50)
    print("API Key সেটআপ")
    print("="*50)
    
    # API প্রোভাইডার নির্বাচন
    print("\nAPI প্রোভাইডার নির্বাচন করুন:")
    print("1. apilayer.com (মাসে 100 ফ্রি রিকুয়েস্ট)")
    print("2. abstractapi.com (মাসে 250 ফ্রি রিকুয়েস্ট)")
    choice = input("আপনার পছন্দ (1/2): ")
    
    if choice == '1':
        config["api_provider"] = "apilayer"
        print("\napilayer.com থেকে API Key পেতে:")
        print("1. https://apilayer.com/marketplace/number_verification-api এ যান")
        print("2. 'Free' প্ল্যান সিলেক্ট করুন")
        print("3. আপনার API Key কপি করুন")
    elif choice == '2':
        config["api_provider"] = "abstractapi"
        print("\nabstractapi.com থেকে API Key পেতে:")
        print("1. https://www.abstractapi.com/phone-validation-api এ যান")
        print("2. 'Start Free' বাটনে ক্লিক করুন")
        print("3. আপনার API Key কপি করুন")
    else:
        print("অবৈধ নির্বাচন, apilayer ডিফল্ট হিসেবে সেট করা হলো")
        config["api_provider"] = "apilayer"
    
    # API Key ইনপুট
    config["api_key"] = input("\nআপনার API Key এন্টার করুন: ").strip()
    save_config(config)
    print("\n✅ API Key সফলভাবে সেট করা হয়েছে!")
    return config

def get_num_info(number, config):
    """ফোন নম্বরের তথ্য রিট্রিভ করুন"""
    api_key = config["api_key"]
    provider = config["api_provider"]
    
    if provider == "apilayer":
        url = f"https://api.apilayer.com/number_verification/validate?number={number}"
        headers = {"apikey": api_key}
    else:  # abstractapi
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={number}"
        headers = {}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            print("\n❌ ত্রুটি: অবৈধ API Key")
            return None
        elif response.status_code == 429:
            print("\n❌ ত্রুটি: API রিকুয়েস্ট লিমিট শেষ")
            return None
        elif response.status_code != 200:
            print(f"\n❌ ত্রুটি: API থেকে রেসপন্স কোড {response.status_code}")
            return None
            
        data = response.json()
        
        # apilayer এবং abstractapi-র রেসপন্স ফরম্যাট ভিন্ন
        if provider == "apilayer":
            valid = data.get('valid', False)
            if not valid:
                print("\n❌ অবৈধ ফোন নম্বর")
                return None
                
            result = {
                "number": data.get('international_format', 'N/A'),
                "valid": data.get('valid', False),
                "local_format": data.get('local_format', 'N/A'),
                "country": f"{data.get('country_name', 'N/A')} ({data.get('country_code', 'N/A')})",
                "location": data.get('location', 'N/A'),
                "carrier": data.get('carrier', 'N/A'),
                "line_type": data.get('line_type', 'N/A')
            }
        else:  # abstractapi
            valid = data.get('valid', False)
            if not valid:
                print("\n❌ অবৈধ ফোন নম্বর")
                return None
                
            result = {
                "number": data.get('international_format', 'N/A'),
                "valid": data.get('valid', False),
                "local_format": data.get('format_local', 'N/A'),
                "country": f"{data.get('country', 'N/A')} ({data.get('country_code', 'N/A')})",
                "location": data.get('location', 'N/A'),
                "carrier": data.get('carrier', 'N/A'),
                "line_type": data.get('type', 'N/A')
            }
        
        return result
        
    except Exception as e:
        print(f"\n❌ ত্রুটি: {str(e)}")
        return None

def main():
    """মেইন প্রোগ্রাম"""
    config = load_config()
    
    # মেনু প্রদর্শন
    print("\n" + "="*50)
    print("ফোন নম্বর ইনফরমেশন চেকার")
    print("="*50)
    
    while True:
        print("\nমেনু:")
        print("1. ফোন নম্বর চেক করুন")
        print("2. API Key সেট করুন")
        print("3. প্রস্থান")
        
        choice = input("আপনার পছন্দ (1/2/3): ")
        
        if choice == '1':
            # API Key চেক করুন
            if not config.get("api_key"):
                print("\n❌ API Key সেট করা হয়নি। প্রথমে API Key সেট করুন")
                config = set_api_key()
                if not config.get("api_key"):
                    continue
            
            # ফোন নম্বর ইনপুট
            number = input("\nফোন নম্বর (দেশ কোড সহ) এন্টার করুন: ").strip()
            if not number:
                print("\n❌ ফোন নম্বর এন্টার করুন")
                continue
                
            # তথ্য রিট্রিভ করুন
            print("\n⏳ তথ্য রিট্রিভ করা হচ্ছে...")
            info = get_num_info(number, config)
            
            # ফলাফল প্রদর্শন
            if info:
                print("\n" + "="*50)
                print("ফোন নম্বরের তথ্য:")
                print("="*50)
                print(f"• নম্বর: {info['number']}")
                print(f"• বৈধতা: {'হ্যাঁ' if info['valid'] else 'না'}")
                print(f"• লোকাল ফরম্যাট: {info['local_format']}")
                print(f"• দেশ: {info['country']}")
                print(f"• লোকেশন: {info['location']}")
                print(f"• অপারেটর: {info['carrier']}")
                print(f"• লাইন টাইপ: {info['line_type']}")
                print("="*50)
        
        elif choice == '2':
            config = set_api_key()
        
        elif choice == '3':
            print("\nপ্রোগ্রাম বন্ধ হচ্ছে...")
            break
        
        else:
            print("\n❌ অবৈধ নির্বাচন, আবার চেষ্টা করুন")

if __name__ == "__main__":
    main()
