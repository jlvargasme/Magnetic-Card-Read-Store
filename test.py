import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
  "api_key": "40cec2ec47605eb09286969b84f5eaeb-us11",
  "server": "us11"
})

response = mailchimp.ping.get()
print(response)

list_id = "4abc78d557"

member_info = {
    "email_address": "jwuxx@umich.edu",
    "status": "subscribed"
}

try:
  #to add a new member
  response = mailchimp.lists.add_list_member(list_id, member_info)

  # to update or insert a member
  # response = mailchimp.lists.set_list_member(list_id, member_info["email_address"], member_info)
  print("response: {}".format(response))
except ApiClientError as error:
  print("An exception occurred: {}".format(error.text))