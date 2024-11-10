import time
from database import initialize_database
from pipeline import run_pipeline


def main():
    db_path = 'all_issuers_data.db'

    # Vreme koga pocnuva programata
    start_time = time.time()
    print("Program started at:", time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(start_time)))

    initialize_database(db_path)
    run_pipeline(db_path)
    end_time = time.time()

    # Vreme koga zavrsuva programata
    print("Program finished at:", time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(end_time)))

    # Vkupno vreme za prevzemanje podatoci
    total_time = end_time - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"Total execution time: {int(minutes)} mins {int(seconds)} sec  ({total_time:.3f} seconds)")


if __name__ == "__main__":
    main()
