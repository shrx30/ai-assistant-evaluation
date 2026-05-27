# ---------------------------------
# Logging Disabled Temporarily
# ---------------------------------

# try:

#     log_data = LogEvent(

#         prompt=str(
#             user_input
#         ),

#         sanitized_prompt=str(
#             sanitized_prompt
#         ),

#         response=str(
#             response
#         ),

#         plan=str(
#             plan
#         ),

#         safe=True
#     )

#     save_log(log_data)

# except Exception as e:

#     print(
#         f"Logging Error: {str(e)}"
#     )