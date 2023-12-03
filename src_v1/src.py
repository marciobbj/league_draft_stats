# -*- coding: iso-8859-1 -*-
import json
import os

from src_v1.models import Champion

from decimal import Decimal, ROUND_HALF_UP


def evaluate_champion_strength(champion):
    # Normalizar as métricas para uma escala de 0 a 1 usando Decimal
    tier_normalized = (Decimal("5") - Decimal(champion.tier)) / Decimal(
        "5"
    )  # Normalizando os tiers de 1 a 5
    win_rate_normalized = Decimal(champion.win_rate) / Decimal("100")
    pick_rate_normalized = Decimal(champion.pick_rate) / Decimal("100")
    ban_rate_normalized = Decimal(champion.ban_rate) / Decimal("100")

    # Aplicar pesos baseados na importância relativa dessas métricas
    weights = {
        "tier": Decimal("0.4"),
        "win_rate": Decimal("0.3"),
        "pick_rate": Decimal("0.2"),
        "ban_rate": Decimal("0.1"),
    }
    total_score = (
        tier_normalized * weights["tier"]
        + win_rate_normalized * weights["win_rate"]
        + pick_rate_normalized * weights["pick_rate"]
        + ban_rate_normalized * weights["ban_rate"]
    ).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP)

    # Retorna as métricas no formato original e a pontuação total
    return {
        "tier_score": int(champion.tier),
        "win_rate_score": float(champion.win_rate),
        "pick_rate_score": float(champion.pick_rate),
        "ban_rate_score": float(champion.ban_rate),
        "total_score": total_score,
    }


def find_strong_matchups(champion, enemy_champions):
    strong_against = []
    for enemy in enemy_champions:
        # Verifica se o campeão não é listado como fraco contra o inimigo
        if enemy.champion not in champion.weak_against:
            # Calcula a diferença nas taxas de vitória como uma métrica de força
            win_rate_diff = float(champion.win_rate) - float(enemy.win_rate)

            # Considera o campeão forte contra o inimigo se a diferença nas taxas de vitória for significativa
            if (
                win_rate_diff > 1.5
            ):  # 'threshold' é um valor definido por você para determinar o que é 'significativo'
                strong_against.append(enemy)

    return strong_against


def check_matchup(champion_one: Champion, champion_two: Champion):
    # Avaliar a força de cada campeão
    champion_one_strength = evaluate_champion_strength(champion_one)
    champion_two_strength = evaluate_champion_strength(champion_two)

    # Ajustar pontuação com base na relação weak_against
    if champion_two.champion in champion_one.weak_against:
        champion_one_strength["total_score"] *= Decimal(
            "0.9"
        )  # Reduz em 10% se for fraco contra
    if champion_one.champion in champion_two.weak_against:
        champion_two_strength["total_score"] *= Decimal(
            "0.9"
        )  # Reduz em 10% se for fraco contra

    # Encontrar matchups fortes
    strong_against_one = find_strong_matchups(champion_one, [champion_two])
    strong_against_two = find_strong_matchups(champion_two, [champion_one])

    # Aumentar pontuação se for forte contra
    is_strong_against_one = False
    is_strong_against_two = False

    if strong_against_one:
        champion_one_strength["total_score"] *= Decimal(
            "1.1"
        )  # Aumenta em 10% se for forte contra
        is_strong_against_one = True
    if strong_against_two:
        champion_two_strength["total_score"] *= Decimal(
            "1.1"
        )  # Aumenta em 10% se for forte contra
        is_strong_against_two = True

    # Calcular a probabilidade de vitória
    total_strength = (
        champion_one_strength["total_score"] + champion_two_strength["total_score"]
    )
    champion_one_win_probability = champion_one_strength["total_score"] / total_strength
    champion_two_win_probability = champion_two_strength["total_score"] / total_strength

    # Construção do resultado final
    output_analysis = {
        "champion_one": {
            "champion": champion_one.champion,
            "tier": champion_one_strength["tier_score"],
            "win_rate": champion_one_strength["win_rate_score"],
            "pick_rate": champion_one_strength["pick_rate_score"],
            "ban_rate": champion_one_strength["ban_rate_score"],
            "total": champion_one_strength["total_score"],
            "win_chance": f"{champion_one_win_probability * 100:.2f}%",
            "is_strong_against": is_strong_against_one,
        },
        "champion_two": {
            "champion": champion_two.champion,
            "tier": champion_two_strength["tier_score"],
            "win_rate": champion_two_strength["win_rate_score"],
            "pick_rate": champion_two_strength["pick_rate_score"],
            "ban_rate": champion_two_strength["ban_rate_score"],
            "total": champion_two_strength["total_score"],
            "win_chance": f"{champion_two_win_probability * 100:.2f}%",
            "is_strong_against": is_strong_against_two,
        },
    }

    return output_analysis


def load_champions():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(
        dir_path, "..", "storage", "opgg", "champion_tier_list.json"
    )

    with open(file_path, "r") as file:
        data = json.load(file)

    return data


def get_champion_stats(champion_name: str):
    champions = load_champions()
    for champion in champions:
        if champion["champion"] == champion_name:
            return champion
    return None


def evaluate_overall_comp(lanes_matchups):
    total_score_blue = 0
    total_score_red = 0
    num_lanes = len(lanes_matchups)

    for lane in lanes_matchups.values():
        total_score_blue += lane['champion_one']['total']
        total_score_red += lane['champion_two']['total']

    average_score_blue = total_score_blue / num_lanes
    average_score_red = total_score_red / num_lanes

    # Calcula a probabilidade de vitória para cada lado
    total_score_both = average_score_blue + average_score_red
    win_rate_blue = (average_score_blue / total_score_both) * 100
    win_rate_red = (average_score_red / total_score_both) * 100

    return {
        "average_score_blue": round(average_score_blue, 5),
        "average_score_red": round(average_score_red, 5),
        "win_rate_blue": round(win_rate_blue, 3),
        "win_rate_red":  round(win_rate_red, 3)
    }