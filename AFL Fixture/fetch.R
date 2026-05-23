library(fitzRoy)
library(dplyr)


player_stats_fryzigg_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "fryzigg")

player_stats_footywire_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "footywire")

player_stats_footywire_2026 <- fetch_player_stats(2026, comp = "AFLM", source = "footywire")

player_stats_AFL_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "AFL")

player_stats_adltables_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "afltables")


clean_stats <- player_stats %>%
  select(
    
  )

fixture <- fetch_fixture(2020, comp = "AFLM")

# Save the selected data to a new variable
clean_fixture <- fixture %>%
  select(
    round.name,
    home.team.name, away.team.name, venue.name
  )

colnames(clean_fixture) <- c("Round", "Home", "Away", "Venue")

# Write to CSV
write.csv(clean_fixture, "C:/Users/dashi/Desktop/AFL-Fantasy-Stats/AFL Fixture/afl_fixture_2020.csv", row.names = FALSE)