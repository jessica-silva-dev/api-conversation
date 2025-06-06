from django.apps import AppConfig
import sys, os




class MatcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matcher'
    
    def ready(self):
        from matcher.job.tranfer_ticket import scheduler
        if 'runserver' in sys.argv and ('--noreload' in sys.argv or os.environ.get("RUN_MAIN") == "true"):
            scheduler.start()    
    
    



        
    
    
