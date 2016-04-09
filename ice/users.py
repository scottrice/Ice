
def locate_eligible_users(steam):
  # No this isn't the bachelorette, `eligible` in this context means "is valid
  # to sync ROMs for". Specifically, we want to ignore the anonymous context,
  # cause theres no reason to sync ROMs for it since you cant log in as them.
  is_user_context = lambda context: context.user_id != 'anonymous'
  return filter(is_user_context, steam_module.local_user_contexts(self.steam))
