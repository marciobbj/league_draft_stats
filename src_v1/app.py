# -*- coding: iso-8859-1 -*-
from flask import Flask, request, render_template, session
from src_v1.forms.src_v1 import RedDraft, BlueDraft
from src_v1.src import load_champions, check_matchup, get_champion_stats, evaluate_overall_comp
from src_v1.models import Champion

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=["GET", "POST"])
def home():
    champions = load_champions()

    blue_draft = BlueDraft(prefix="blue")
    red_draft = RedDraft(prefix="red")

    blue_draft.set_choices(champions)
    red_draft.set_choices(champions)

    if request.method == "POST":
        if "restore_draft" in request.form:
            # Restaurar dados do último draft
            last_draft = session.get("last_draft", None)
            if last_draft:
                red_draft.process(data=last_draft["red"])
                blue_draft.process(data=last_draft["blue"])
        elif red_draft.validate_on_submit() and blue_draft.validate_on_submit():
            red_side_choices = red_draft.data
            blue_side_choices = blue_draft.data
            top_matchup = check_matchup(
                Champion(**get_champion_stats(blue_side_choices["top"])),
                Champion(**get_champion_stats(red_side_choices["top"])),
            )
            mid_matchup = check_matchup(
                Champion(**get_champion_stats(blue_side_choices["mid"])),
                Champion(**get_champion_stats(red_side_choices["mid"])),
            )
            jungle_matchup = check_matchup(
                Champion(**get_champion_stats(blue_side_choices["jungle"])),
                Champion(**get_champion_stats(red_side_choices["jungle"])),
            )
            adc_matchup = check_matchup(
                Champion(**get_champion_stats(blue_side_choices["adc"])),
                Champion(**get_champion_stats(red_side_choices["adc"])),
            )
            support_matchup = check_matchup(
                Champion(**get_champion_stats(blue_side_choices["support"])),
                Champion(**get_champion_stats(red_side_choices["support"])),
            )
            lanes = {
                "Top": top_matchup,
                "Mid": mid_matchup,
                "Jungle": jungle_matchup,
                "ADC": adc_matchup,
                "Support": support_matchup,
            }
            overall_comp_points = evaluate_overall_comp(lanes)
            app.logger.info("Matchup Analysis: %s", lanes)
            session["last_draft"] = {"red": red_side_choices, "blue": blue_side_choices}
            return render_template("src_v1/lane_matchup_analysis.html", lanes=lanes, overall_comp_points=overall_comp_points)

    # Verifica se existe um último draft salvo na sessão
    draft_saved = "last_draft" in session

    return render_template(
        "src_v1/home.html",
        blue_draft=blue_draft,
        red_draft=red_draft,
        draft_saved=draft_saved,
    )
