rm(list = ls())
true_beta = 2
true_gamma = 1
true_rho = 0.25
true_i0 = 0.01
true_rho = 0.25
true_N = 100

complete_pars <- function(beta = true_beta, gamma = true_gamma, N = true_N, 
                          i0 = true_i0, rho = true_rho, duration = 20, dt = 1){
  pars = data.frame(beta = beta, gamma = gamma, N = N,
                    i0 = i0, rho = rho, duration = duration, dt = dt)
  return(pars)
}

run_SIR <- function(pars){
  beta = pars[['beta']]
  gamma = pars[['gamma']]
  N = pars[['N']]
  i0 = pars[['i0']]
  rho = pars[['rho']]
  dt = pars[['dt']]
  duration = pars[['duration']]
  dt = pars[['dt']]
  times = seq(0,duration, by = dt)
  SIR_df = data.frame(time = times, 
                      S = 0, I = 0, R = 0, newI = 0, newC = 0)
  SIR_df$I[1] <- round(i0*N)
  SIR_df$S[1] <- N - SIR_df$I[1]
  
  for (t_num in seq_along(head(times, -1))){
    S = SIR_df$S[t_num]
    I = SIR_df$I[t_num]
    R = SIR_df$R[t_num]
    #
    newI = round(S * (1 - exp(-beta * I / N * dt)))
    newR = round(I * (1 - exp(-gamma * dt)))
    newC = rbinom(1, newI, prob = rho)
    #
    SIR_df$S[t_num + 1] = S - newI
    SIR_df$I[t_num + 1] = I + newI - newR
    SIR_df$R[t_num + 1] = R + newR
    SIR_df$newI[t_num] = newI
    SIR_df$newC[t_num] = newC
  }
  return(SIR_df)
}

true_pars = complete_pars()
true_df = run_SIR(true_pars)

require(RColorBrewer)

SIR_COLS = brewer.pal(4, 'Set1')[c(3, 1, 2, 4)]

obs_weeks = 2:7
obs_df <- true_df[which(true_df$time %in% obs_weeks), c("time", "newC")]

plot_sir = function(df, rho){
  time = df[['time']]
  S = df[['S']]
  I = df[['I']]
  R = df[['R']]
  newI = df[['newI']]
  
  obs_weeks = obs_df[['time']]
  #
  plot(time, S, type = 'l', xlab = 'Time', ylab = 'Population', ylim = c(0, max(S+I+R)), lwd = 2, col = SIR_COLS[1])
  lines(time, I, lwd = 2, col = SIR_COLS[2])
  lines(time, R, lwd = 2, col = SIR_COLS[3])
  #
  obs_locs <- which(time %in% obs_weeks)
  plot(time, newI, col = SIR_COLS[2], pch = 19)
  points(obs_df$time, obs_df$newC, col = SIR_COLS[4], pch = 4, lwd = 2)
  points(time[obs_locs], rho * newI[obs_locs], col = SIR_COLS[2], cex = 2, lwd = 2)
}

plot_likelihood <- function(rho, newI, newC, tol = 1e-1){
  prob_df = data.frame(obs = 0:newI,
                       prob = dbinom(0:newI, newI, prob = rho))
  prob_df$rel_prob = prob_df$prob / max(prob_df$prob)
  xmin <- max(min(min(which(prob_df$rel_prob > tol))-1, newC - 5), 0)
  xmax <- min(max(max(which(prob_df$rel_prob > tol)), newC + 5), newI)
  prob_df$keep <- 0
  prob_df$keep[xmin:xmax] <- 1
  prob_df$COL <- 1
  prob_df$COL[which(prob_df$obs == newC)] <- 2
  COLS <- c(rgb(0,0,0,.1), 2)
  barplot(prob_df$prob[prob_df$keep == 1], col = COLS[prob_df$COL[prob_df$keep == 1]])
}

get_ll = function(rho, df, obs_df){
  obs_weeks = obs_df[['time']]
  #
  newC_vec = obs_df[['newC']]
  newI_vec <- df[['newI']][which(df[['time']] %in% obs_weeks)]
  #
  ll = sum(dbinom(newC_vec, newI_vec, prob = rho, log = TRUE))
  #
  return(ll)
}

plot_obs <- function(rho, df, obs_df){
  obs_weeks = obs_df[['time']]
  for (o_num in seq_along(obs_weeks)){
    tmp_newI <- df$newI[which(df$time == obs_weeks[o_num])]
    tmp_newC <- obs_df$newC[which(obs_df$time == obs_weeks[o_num])]
    plot_likelihood(rho, tmp_newI, tmp_newC)
  }
}

plot_lls <- function(current, history){
  ll_vec <- history[['ll_vec']]
  best_ll <- history[['best']][['ll']]
  n_track <- length(ll_vec)
  #
  plot(ll_vec, xlim = c(0, n_track + 2),
       ylim = c(min(ll_vec, na.rm = TRUE),
                best_ll), pch = 19)
  abline(v = n_track + 1, lty = 2)
  points(n_track + 2, best_ll, pch = 4, lwd = 2)
}


update_plot <- function(current, history, obs_df){
  panels = c(1, 3, 4, 5, 1, 3, 4, 5,
             1, 6, 7, 8, 2, 6, 7, 8,
             2, 9, 9, 9, 2, 9, 9, 9)
  
  layout(matrix(panels, 6, 4, byrow = TRUE),
         widths = c(3,1,1,1)) 
  par(mar=c(5.1,5.1,1.1,2.1), oma = c(0,0,3,2))
  plot_sir(current[['df']], current[['pars']][['rho']])
  par(mar=c(2.1,2.1,1.1,.1))  
  plot_obs(current[['pars']][['rho']], current[['df']], obs_df)
  #
  par(mar = c(5.1,2.1,2.1,.1))
  plot_lls(current, history)
}

run_pars <- function(pars, obs_df){
  df = run_SIR(pars)
  ll = get_ll(pars[['rho']], df, obs_df)
  return(list(ll = ll, pars = pars, df = df))
}

init_best = function(init_pars, n_track, obs_df){
  df = run_SIR(init_pars)
  ll <- get_ll(init_pars[['rho']], df, obs_df)
  # 
  return(list(ll_vec = rep(NA, n_track),
              best = list(ll = ll, pars = init_pars, df = df)))
}


update_history <- function(current, history){
  current_ll <- current[['ll']]
  #
  ll_vec <- history[['ll_vec']]
  best_ll <- history[['best']][['ll']]
  n_track <- length(ll_vec)
  length_not_na_lls <- length(which(!is.na(ll_vec)))
  #
  if (length_not_na_lls < n_track){
    ll_vec[length_not_na_lls + 1] <- current_ll
  } else {
    ll_vec <- c(ll_vec[-1], current_ll)
  }
  history[['ll_vec']] <- ll_vec
  #
  if (current_ll > best_ll){
    history[['best']] = list(ll = current_ll, pars = current['pars'], df = current['df'])
  }
  return(history)
}

run_guess <- function(guess_pars, history, obs_df){
  current <- run_pars(guess_pars, obs_df)
  history <- update_history(current, history)
  update_plot(current, history, obs_df)
  return(history)
}

n_track = 10

init_beta = 1.8
init_gamma = 1.1
init_rho = 0.5
history = init_best(complete_pars(beta = init_beta, 
                                  gamma = init_gamma, 
                                  rho = init_rho),
                    n_track, obs_df)
############
# Start here
############

guess_beta = 1.8
guess_gamma = 1.1
guess_rho = 0.5


history <- run_guess(complete_pars(beta = guess_beta,
                                   gamma = guess_gamma,
                                   rho = guess_rho), history, obs_df)
guess_beta = 2
guess_gamma = 1
guess_rho = 0.25


history <- run_guess(complete_pars(beta = guess_beta,
                                   gamma = guess_gamma,
                                   rho = guess_rho), history, obs_df)
