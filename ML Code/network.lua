require 'optim'
require 'image'
require 'nn'


--------------------------------------------------------------------------
-- Read Database --
--------------------------------------------------------------------------

print"---------------------Welcome to the -zare3- AA detector---------------------"


print 'Loading Train Database ...'
-- Load Training Data


relativePath = "/"
-- 1468 +  1681
trainData = {
  data = torch.Tensor(3147, 3981),
  labels = torch.Tensor(3147),
  size = function()
    return 3147
  end
}

files = {"adult","non-adult"}
articleCnt = 1
for idx = 1, 2 do 
  for i in io.popen("ls /"  .. files[idx]):lines()  do
     if string.find(i,"%.txt$") then
      filePath = relativePath .. files[idx] .. '/' .. i
      local f, err = io.open(filePath)
      if not f then print (err) end
          local l, err = f:read()
      if not l then print (err) break end
      dictIdx = 1
          for i in string.gmatch(l, "%S+") do
        trainData.data[articleCnt][dictIdx] = tonumber(i)
        dictIdx = dictIdx + 1
      end
      f:close()
     end
     trainData.labels[articleCnt] = idx
     articleCnt = articleCnt + 1
  end
end

mean_u = trainData.data[{ {},{} }]:mean()
std_u = trainData.data[{ {},{} }]:std()
trainData.data[{ {},{}}]:add(-mean_u)
trainData.data[{ {},{} }]:div(-std_u)

print ("MEAN IS: " .. mean_u .. " SUBTRACTING .. ")
print ("STDEVIATION IS: " .. std_u .. " SUBTRACTING .. ")





print "--------------------------------------------------------------------"

print 'Loading Test Database ...'
-- Load Testing Data

testData = {
  data = torch.Tensor(3002, 3981),
  labels = torch.Tensor(3002),
  size = function()
    return 3002
  end
}



files = {"adult","non-adult"}
articleCnt = 1
for idx = 1, 2 do 
  for i in io.popen("ls /test/" .. files[idx]):lines()  do
     if string.find(i,"%.txt$") then
      filePath = relativePath .. "test/" .. files[idx] .. '/' .. i
      local f, err = io.open(filePath)
      if not f then print (err) end
          local l, err = f:read()
      if not l then print (err) break end
      dictIdx = 1
          for i in string.gmatch(l, "%S+") do
        testData.data[articleCnt][dictIdx] = tonumber(i)
        dictIdx = dictIdx + 1
      end
      f:close()
     end
     print (articleCnt .. " " .. filePath)
     testData.labels[articleCnt] = idx
     articleCnt = articleCnt + 1
  end
end


--testData.data = trainData.data
--testData.labels = trainData.labels

mean_u = testData.data[{ {},{} }]:mean()
std_u = testData.data[{ {},{} }]:std()
testData.data[{ {},{}}]:add(-mean_u)
testData.data[{ {},{} }]:div(-std_u)

print ("MEAN IS: " .. mean_u .. " SUBTRACTING .. ")
print ("STDEVIATION IS: " .. std_u .. " SUBTRACTING .. ")





-- ignore setmetatable for now, it is a feature beyond the scope of this tutorial. It sets the index operator.
setmetatable(trainData, 
    {__index = function(t, i) 
                    return {t.data[i], t.labels[i]} 
                end}
);
trainData.data = trainData.data:double() -- convert the data from a ByteTensor to a DoubleTensor.

function trainData:size() 
    return self.data:size(1) 
end



-- ignore setmetatable for now, it is a feature beyond the scope of this tutorial. It sets the index operator.
setmetatable(testData, 
    {__index = function(t, i) 
                    return {t.data[i], t.labels[i]} 
                end}
);                                            
testData.data = testData.data:double() -- convert the data from a ByteTensor to a DoubleTensor.

function testData:size() 
    return self.data:size(1) 
end


print "------------------START -- 3981/500/500 --- 55 -0.01- TRAINING ------------------"



mlp = nn.Sequential();  -- make a multi-layer perceptron

inputs = 3981; outputs = 2; HUs = 1000; -- parameters
mlp:add(nn.Linear(inputs, HUs))
mlp:add(nn.Tanh())                                                                                                                                                                                                                                                                                                                                                        
mlp:add(nn.Linear(HUs, outputs))
mlp:add(nn.LogSoftMax())

criterion = nn.ClassNLLCriterion()  
criterion = criterion
trainData.data = trainData.data
trainer = nn.StochasticGradient(mlp, criterion)
trainer.learningRate = 0.01
trainer.maxIteration = 55
trainer:train(trainData)



print "------------------START -- 3981/500/500 --- 55 -0.01- TESTING ------------------"



correct = 0
for i=1,3002 do
    local groundtruth = testData.labels[i]
    local prediction = mlp:forward(testData.data[i])
    local confidences, indices = torch.sort(prediction, true)  -- true means sort in descending order
    if groundtruth == indices[1] then
        correct = correct + 1
    end
end

print(correct, 100*correct/3002 .. ' % ')














