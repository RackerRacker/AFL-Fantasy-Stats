library(fitzRoy)
library(dplyr)


player_stats_fryzigg_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "fryzigg")

player_stats_footywire_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "footywire")

player_stats_footywire_2026 <- fetch_player_stats(2026, comp = "AFLM", source = "footywire")

player_stats_AFL_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "AFL")

player_stats_adltables_2025 <- fetch_player_stats(2025, comp = "AFLM", source = "afltables")


# Move positions from AFL -> adltables
updated_player_stats_2025_df <- left_join(player_stats_adltables_2025, player_stats_AFL_2025, by="")

# Save the selected data to a new variable
clean_fixture <- fixture %>%
  select(
    round.name,
    home.team.name, away.team.name, venue.name
  )

colnames(clean_fixture) <- c("Round", "Home", "Away", "Venue")

head(player_stats_AFL_2025)
clean_AFL_df <- player_stats_AFL_2025 %>%
  select(
    round.roundNumber, venue.name, home.team.club.name, away.team.club.name, player.jumperNumber, player.player.position,
    player.player.player.givenName, player.player.player.surname
  )

# Write to CSV
write.csv(clean_AFL_df, "player_stats_AFL.csv", row.names = FALSE)