import matplotlib.pyplot as plt
import os

def plot_ecl_curve(df, segment, save_dir="app/static"):
    seg_df = df[df["segment"].str.upper() == segment.upper()]
    if seg_df.empty:
        raise ValueError("Segment not found")

    plt.figure(figsize=(8,5))
    plt.plot(seg_df["segment"], seg_df["avg_ecl"], marker="o", linewidth=2)
    plt.title(f"ECL Curve - {segment}")
    plt.xlabel("Segment")
    plt.ylabel("Expected Credit Loss (₹)")
    plt.grid(True)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"ecl_curve_{segment}.png")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    return file_path
