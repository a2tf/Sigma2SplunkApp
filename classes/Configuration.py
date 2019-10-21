class Configuration:

    def __init__(self, config):
        # Write Sigma2SplunkApp Configuration
        if "splunk_path" in config["Sigma2SplunkApp"]:
            self.splunk_path = config["Sigma2SplunkApp"]["splunk_path"]
        else:
            self.splunk_path = "/opt/splunk"
        if "whitelist_app" in config["Sigma2SplunkApp"]:
            self.whitelist_app = config["Sigma2SplunkApp"]["whitelist_app"]
        if "destination_app" in config["Sigma2SplunkApp"]:
            self.destination_app = config["Sigma2SplunkApp"]["destination_app"]
        if "git_path" in config["Sigma2SplunkApp"]:
            self.git_path = config["Sigma2SplunkApp"]["git_path"]
        else:
            self.git_path = "~/git"
            
        # Write Sigma2SplunkAlert Configuration
        if "standard_config" in config["Sigma2SplunkAlert"]:
            self.S2SA_standard_config = config["Sigma2SplunkAlert"]["standard_config"]
        else:
            self.S2SA_standard_config = "config.yml"
        if "whitelist_config" in config["Sigma2SplunkAlert"]:
            self.S2SA_whitelist_config = config["Sigma2SplunkAlert"]["whitelist_config"]
        if "template" in config["Sigma2SplunkAlert"]:
            self.S2SA_template_config = config["Sigma2SplunkAlert"]["template"]
        else:
            self.S2SA_template_config = "template"        
        
        # Write Sigma Configuration
        if "sigma_config" in config["sigma"]:
            self.sigma_config = config["sigma"]["sigma_config"]
        else:
            self.sigma_config = "splunk-all.yml"
        self.sigma_rules = []
        self.sigma_rules_whitelist = []
        if "sigma_rules" in config["sigma"]:
            self.sigma_rules = config["sigma"]["sigma_rules"]
        if "sigma_rules_whitelist" in config["sigma"]:
            self.sigma_rules_whitelist = config["sigma"]["sigma_rules_whitelist"]
        if "sigma_rules_skipping" in config["sigma"]:
            self.sigma_rules_skipping = config["sigma"]["sigma_rules_skipping"]
        else:
            self.sigma_rules_skipping = []
        
        
            