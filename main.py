from display import draw_start_screen, draw_main_screen, draw_done_screen
from cards import load_cards, save_cards, get_due_cards, answer_card, start_new_session
import os
import time

ON_PI = os.path.exists('/sys/firmware/devicetree/base/model')

if ON_PI:
    import lgpio
    h = lgpio.gpiochip_open(0)
    for pin in [5, 6, 13, 19]:
        lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_UP)

def wait_for_button():
    if ON_PI:
        while True:
            if lgpio.gpio_read(h, 5) == 0:
                time.sleep(0.2)
                return "show"
            if lgpio.gpio_read(h, 6) == 0:
                time.sleep(0.2)
                return "know"
            if lgpio.gpio_read(h, 13) == 0:
                time.sleep(0.2)
                return "again"
            if lgpio.gpio_read(h, 19) == 0:
                time.sleep(0.2)
                return "exit"
    else:
        answer = input("(s)how / (k)now / (a)gain / (e)xit: ")
        mapping = {"s": "show", "k": "know", "a": "again", "e": "exit"}
        return mapping.get(answer.lower(), "show")

def run():
    while True:
        cards = load_cards()
        due = get_due_cards(cards)
        draw_start_screen(cards_today=len(due))

        if ON_PI:
            while lgpio.gpio_read(h, 5) == 1:
                time.sleep(0.1)
        else:
            input("Press Enter to start...")

        print(f"Due cards: {len(due)}")
        queue = list(due)
        total = len(queue)
        answered = 0
        exited = False

        while queue and not exited:
            card = queue.pop(0)
            answered += 1
            draw_main_screen(
                word=card["word"],
                translation=card["translation"],
                card_num=answered,
                total=total,
                show_translation=False
            )
            while True:
                action = wait_for_button()
                if action == "exit":
                    exited = True
                    break
                if action == "show":
                    draw_main_screen(
                        word=card["word"],
                        translation=card["translation"],
                        card_num=answered,
                        total=total,
                        show_translation=True
                    )
                if action == "know":
                    answer_card(card, True)
                    break
                if action == "again":
                    answer_card(card, False)
                    queue.append(card)
                    total += 1
                    break


        if not exited:
            cards = start_new_session(cards)

        save_cards(cards)
        draw_done_screen()
        print("Done! Cards saved.")

        if ON_PI:
            while lgpio.gpio_read(h, 19) == 1:
                time.sleep(0.1)
        else:
            input("Press Enter to return to start...")

run()