# import streamlit as st
# from supabase import create_client, Client

# # ---------------------------------------------------
# # SUPABASE CLIENT INITIALIZATION
# # ---------------------------------------------------

# @st.cache_resource
# def init_supabase() -> Client:
#     """Create and cache the Supabase client using Streamlit secrets."""
#     url = st.secrets["supabase"]["url"]
#     key = st.secrets["supabase"]["key"]
#     return create_client(url, key)


# # ---------------------------------------------------
# # AUTH HELPERS
# # ---------------------------------------------------

# def sign_up(email: str, password: str) -> dict:
#     """
#     Register a new user with email and password.
#     Returns {"success": True, "user": user_obj} or {"success": False, "error": "message"}.
#     """
#     try:
#         supabase = init_supabase()
#         response = supabase.auth.sign_up({
#             "email": email,
#             "password": password,
#         })
#         if response.user:
#             return {"success": True, "user": response.user}
#         else:
#             return {"success": False, "error": "Sign-up failed. Please try again."}
#     except Exception as e:
#         error_msg = str(e)
#         if "already registered" in error_msg.lower() or "already been registered" in error_msg.lower():
#             return {"success": False, "error": "This email is already registered. Please log in instead."}
#         elif "password" in error_msg.lower() and ("short" in error_msg.lower() or "weak" in error_msg.lower() or "least" in error_msg.lower()):
#             return {"success": False, "error": "Password is too weak. Use at least 6 characters."}
#         elif "invalid" in error_msg.lower() and "email" in error_msg.lower():
#             return {"success": False, "error": "Please enter a valid email address."}
#         elif "rate" in error_msg.lower() or "security purposes" in error_msg.lower() or "seconds" in error_msg.lower():
#             return {"success": False, "error": error_msg}
#         else:
#             return {"success": False, "error": f"Sign-up failed: {error_msg}"}


# def sign_in(email: str, password: str) -> dict:
#     """
#     Sign in an existing user with email and password.
#     Returns {"success": True, "user": user_obj, "session": session_obj}
#     or {"success": False, "error": "message"}.
#     """
#     try:
#         supabase = init_supabase()
#         response = supabase.auth.sign_in_with_password({
#             "email": email,
#             "password": password,
#         })
#         if response.session:
#             return {
#                 "success": True,
#                 "user": response.user,
#                 "session": response.session,
#             }
#         else:
#             return {"success": False, "error": "Login failed. Please check your credentials."}
#     except Exception as e:
#         error_msg = str(e)
#         if "invalid" in error_msg.lower() and ("credentials" in error_msg.lower() or "login" in error_msg.lower()):
#             return {"success": False, "error": "Invalid email or password."}
#         elif "email not confirmed" in error_msg.lower():
#             return {"success": False, "error": "Please confirm your email before logging in. Check your inbox."}
#         elif "rate" in error_msg.lower():
#             return {"success": False, "error": "Too many attempts. Please wait a moment and try again."}
#         else:
#             return {"success": False, "error": f"Login failed: {error_msg}"}


# def reset_password(email: str) -> dict:
#     """
#     Send a password reset email.
#     Returns {"success": True} or {"success": False, "error": "message"}.
#     """
#     try:
#         supabase = init_supabase()
#         supabase.auth.reset_password_for_email(email)
#         return {"success": True}
#     except Exception as e:
#         error_msg = str(e)
#         if "rate" in error_msg.lower():
#             return {"success": False, "error": "Too many requests. Please wait before trying again."}
#         elif "invalid" in error_msg.lower() and "email" in error_msg.lower():
#             return {"success": False, "error": "Please enter a valid email address."}
#         else:
#             return {"success": False, "error": f"Failed to send reset email: {error_msg}"}


# def sign_out():
#     """Sign out the current user and clear session state."""
#     try:
#         supabase = init_supabase()
#         supabase.auth.sign_out()
#     except Exception:
#         pass  # Clear local state regardless

#     # Clear all auth-related session state
#     keys_to_clear = [
#         "authenticated", "user", "user_email",
#     ]
#     for key in keys_to_clear:
#         if key in st.session_state:
#             del st.session_state[key]


# def get_current_user():
#     """Return the current authenticated user from session state, or None."""
#     if st.session_state.get("authenticated"):
#         return st.session_state.get("user")
#     return None


# def is_authenticated() -> bool:
#     """Check if a user is currently authenticated."""
#     return st.session_state.get("authenticated", False)
