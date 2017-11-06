import WaApi
import urllib.parse
import creds

def get_active_members():
    params = {'$filter': 'member eq true',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts


def print_contact_info(contact):
    print('Contact details for ' + contact.DisplayName + ', ' + contact.Email)
    print('Main info:')
    print('\tID:' + str(contact.Id))
    print('\tFirst name:' + contact.FirstName)
    print('\tLast name:' + contact.LastName)
    print('\tEmail:' + contact.Email)
    print('\tAll contact fields:')
    for field in contact.FieldValues:
        if field.Value is not None:
            print('\t\t' + field.FieldName + ':' + repr(field.Value))



# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
api = WaApi.WaApiClient("APIKEY", creds.APIKEY)
api.authenticate_with_apikey(creds.APIKEY)
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

print(account.PrimaryDomainName)

contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url

active_members = []

# get top 10 active members and print their details
contacts = get_active_members()
for contact in contacts:
    # Print all contact info
    #print_contact_info(contact)

    member = {}
    member["name"] = contact.DisplayName

    for field in contact.FieldValues:
        if field.Value is not None:
            if(field.FieldName == "Membership status"):
                member["level"] = field.Value.Label
            if field.FieldName == "key_card_number":
                member["key"] = field.Value


    if "level" in member and member["level"] != "Lapsed":
        active_members.append(member)


print(active_members)