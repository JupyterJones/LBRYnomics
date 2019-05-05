import fetch_data
import numpy as np
import showresults
import subprocess
import yaml

# List of channels to make forecasts for
channels = sorted(["@Lunduke", "@NaomiBrockwell", "@TheLinuxGamer",
                   "@TheCryptoLark", "@CryptoCandor", "@mikenayna",
                   "@TechFox", "@GaminGHD",
                   "@MinutePhysics", "@GamesGlitches",
                   "@upside", "@OpenSourceGames", "@paulvanderklay",
                   "@JordanBPeterson", "@Crypt0", "@MothersBasement",
                   "@imineblocks", "@tioaventurabus", "@leckakay", "@Luke",
                   "@akirathedon", "@davidpakman", "@timcast", "@AntiMedia",
                   "@water", "@bitcoinandfriends", "@ShutupAndPlay",
                   "@reenthused", "@CatholicHomilies", "@NameThatTune",
                   "@TipWhatYouLike", "@MusicPlanet",
                   "@3Blue1Brown", "@altcoinbuzz", "@BrendonBrewer",
                   "@anton#1c10545675c9d25749fc12f6e872777da257dd51",
                   "@LBRY-Social",
                   "@zO-Music", "@KhanAcademy", "@Michaelcraigheadart",
                   "@postjazzrdg",
                   "@DanielSibisan", "@jeradhill", "@JuliaGalef",
                   "@NorVegan", "@VeganGains", "@UCBerkeley",
                   "@KJamesElliott#36aab723dc34a5e5d4173436f01c7c3457493201",
                   "@veritasium", "@radiodrama", "@inspirationart",
                   "@Archaeosoup", "@eevblog", "@FEEOrg",
                   "@adrianbonillap#2f10475ee7090d2030ee2dd17eb4b39bc9437970",
                   "@ronnietucker", "@mru",
                   "@UCurU6GLM4ggcLtWWAOTzlYw", "@roshansuares",
                   "@Books", "@AlasLewisAndBarnes"],
                    key=lambda s: s.lower())

# Open output CSV file
f = open("forecasts.csv", "w")
f.write("channel_name,months_since_first_tip,num_tips,lbc_received,lbc_per_month,forecast_low,forecast_medium,forecast_high,notes\n")
f.flush()

for channel in channels:
    fetch_data.data_to_yaml(channel)

    yaml_file = open("data.yaml")
    data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    src = data["src"]
    yaml_file.close()
    yaml_file = open(src)
    data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    yaml_file.close()

    subprocess.call(["./main", "-t 10"])
    quantiles = showresults.postprocess()

    f.write(channel + ",")
    duration = data["t_end"] - data["t_start"]
    f.write(str(np.round(duration, 2)) + ",")

    tot = 0.0
    if data["amounts"] is not None and len(data["amounts"]) > 0:
        for amount in data["amounts"]:
            tot += float(amount) # Sometimes yaml thinks it's a string

    f.write(str(len(data["amounts"])) + ",")
    f.write(str(np.round(tot, 2)) + ",")
    f.write(str(np.round(tot/duration, 2)) + ",")
    f.write(str(np.round(quantiles[0], 2)) + ",")
    f.write(str(np.round(quantiles[1], 2)) + ",")
    f.write(str(np.round(quantiles[2], 2)) + ",")

    if duration < 1.0:
        f.write("< 1 month history available, likely unreliable forecast")
    f.write("\n")
    f.flush()

f.close()

