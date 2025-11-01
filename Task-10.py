facts = [
    "john_is_cold.",              
    "raining.",                   
     
    "john_Forgot_His_Raincoat.",  
    "fred_lost_his_car_keys.",    
    "peter_footballer."           
     
]


def verify_fact(fact):
    
    fact = fact.rstrip(".")
    
    if fact.lower() == "john_forgot_his_raincoat":
        return True
    elif fact.lower() == "raining":
        return True
    elif fact.lower() == "foggy":
        return True
    elif fact.lower() == "cloudy":
        return False  
    else:
        return False


for fact in facts:
    
    if not fact or fact.startswith("#"):
        continue
    if verify_fact(fact):
        print(f"{fact} - Yes")
    else:
        print(f"{fact} - No")
